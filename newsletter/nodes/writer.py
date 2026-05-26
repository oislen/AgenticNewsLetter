import logging
from langchain_aws import ChatBedrock
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableConfig

from state import NewsletterState
from utils import style_guides

def writer_node(state: NewsletterState, config: RunnableConfig):
    """
    This node takes the research data collated by the researcher node and generates a newsletter draft using the Bedrock Chat model. It constructs a prompt that includes the research data and a style guide, invokes the language model to generate the newsletter content, and handles any potential guardrail blocks gracefully.

    Parameters
    ----------
    state : NewsletterState
        The current state of the newsletter generation process, which includes the research data and other relevant information.
    config : RunnableConfig
        The configuration object that contains any necessary parameters for the writer node, such as API clients and model identifiers.

    Returns
    --------
    dict
        A dictionary containing the generated newsletter draft and the steps taken by the writer node.
    """
    logging.info("Starting writer node ...")
    logging.info("Initiating Bedrock Chat model ...")
    # Initialize the model with Guardrail integration
    llm = ChatBedrock(
        client=state["bedrock_client"],
        model_id=state["bedrock_model_id"],
        model_kwargs={
            "temperature": 0.7,
            "max_tokens": 2048,
            #"guardrailIdentifier": "your-guardrail-id-here", # From AWS Console
            #"guardrailVersion": "1", # Use a specific version or "DRAFT"
            #"trace": "enabled" # Helpful for debugging why a response was blocked
        }
    )
    # determine selected style
    selected_style = style_guides.get(state.get("style", "ELI5"))
    # System prompt: persona, audience, output contract, anti-hallucination
    # guardrail. Human prompt: today's beat plus the raw research, with
    # citation guidance so URLs from the research are surfaced in the draft.
    system_message = (
        "You are the editor of \"DS Pulse\", a concise personal newsletter "
        "that keeps a busy technically-minded reader current on developments "
        f"in {state['topic']}. Each issue prioritizes substantive signal over "
        "hype: what changed, why it matters, and what to read or try next.\n\n"
        f"Style guide for this issue: {selected_style}\n\n"
        "Output requirements:\n"
        "- Write valid Markdown (it will be rendered to HTML for email).\n"
        "- Open with a short, punchy H1 headline.\n"
        "- Follow with a 2-3 sentence overview of the most important "
        "developments.\n"
        "- Then 3-5 sections, each with an H2 header, summarizing a single "
        "story or theme in 2-4 sentences. Cite the source the first time "
        "you reference a story using an inline Markdown link to the URL "
        "from the research.\n"
        "- Close with a short \"What to watch\" paragraph or takeaway.\n"
        "- Use only facts present in the provided research; do not invent "
        "details, statistics, dates, or attributions. If coverage is thin, "
        "say so honestly rather than padding.\n"
        "- Aim for roughly 400-700 words."
    )
    human_message = (
        f"Today's beat: {state['topic']} — {state['subtopic']}.\n\n"
        "Write today's issue using the research collected below. Each item "
        "includes a title, URL, and content snippet — link the URL inline "
        "the first time you reference a story.\n\n"
        "--- RESEARCH ---\n"
        f"{state['research_data']}\n"
        "--- END RESEARCH ---"
    )
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("human", human_message),
    ])
    try:
        logging.info("Invoking language model ...")
        model_response = llm.invoke(prompt.format(data=state['research_data']))
        response = {"newsletter_draft": model_response.content}
    except Exception as e:
        logging.error(f"Error during model invocation: {e}")
        # If the guardrail triggers a block, handle it gracefully
        response = {"newsletter_draft": "Content blocked by safety guardrails.", "steps_taken": ["blocked"]}
    return response