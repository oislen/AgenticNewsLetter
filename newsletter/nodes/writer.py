import logging
from langchain_aws import ChatBedrock
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableConfig

from state import NewsletterState
from utils import style_guides

def writer_node(state: NewsletterState, config: RunnableConfig):
    """
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
    # The rest of your chain remains the same
    prompt = ChatPromptTemplate.from_messages([
        ("system", f"You are a specialized personal News Letter writer. Style Guide: {selected_style}"),
        ("human", f"Transform this research into a newsletter about {state['topic']} - {state['subtopic']}:\n\n{state['research_data']}")
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