from langchain_aws import ChatBedrock
from langchain_core.prompts import ChatPromptTemplate

from state import NewsletterState
from utils import bedrock_client, style_guides

def writer_node(state: NewsletterState):
    # Initialize the model with Guardrail integration
    bedrock_runtime = bedrock_client()
    llm = ChatBedrock(
        client=bedrock_runtime,
        model_id="eu.anthropic.claude-sonnet-4-5-20250929-v1:0",
        model_kwargs={
            "temperature": 0.7,
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
            ("human", f"Transform this research into a newsletter about {state['topic']}:\n\n{state['research_data']}")
        ])
    
    try:
        response = llm.invoke(prompt.format(data=state['research_data']))
        return {"newsletter_draft": response.content}
    except Exception as e:
        # If the guardrail triggers a block, handle it gracefully
        return {"newsletter_draft": "Content blocked by safety guardrails.", "steps_taken": ["blocked"]}