
import boto3
from langchain_aws import ChatBedrock
from langchain_core.prompts import ChatPromptTemplate

from state import NewsletterState

def writer_node(state: NewsletterState):
# 1. Initialize the Bedrock Runtime client
    bedrock_runtime = boto3.client(
        service_name="bedrock-runtime",
        region_name="us-east-1"
    )
    # Initialize the model with Guardrail integration
    llm = ChatBedrock(
        client=bedrock_runtime,
        model_id="amazon.nova-pro-v1:0",
        model_kwargs={
            "temperature": 0.7,
            "guardrailIdentifier": "your-guardrail-id-here", # From AWS Console
            "guardrailVersion": "1", # Use a specific version or "DRAFT"
            "trace": "enabled" # Helpful for debugging why a response was blocked
        }
    )

# Define style-specific instructions
    style_guides = {
        "academic": (
            "Write in the style of a formal Literature Review. Use objective language, "
            "focus on methodology, architectural innovations, and statistical significance. "
            "Organize by 'Current Research Landscape' and 'Theoretical Implications'."
        ),
        "ELI5": (
            "Explain like I'm five. Use simple analogies, avoid jargon, and focus on "
            "the 'why this matters' for everyday life. Use emojis and a friendly, "
            "storytelling tone."
        ),
        "tutorial": (
            "Focus strictly on implementation. For every news item, include a 'Quick Start' "
            "Python snippet or a CLI command. Prioritize library updates and code examples "
            "over high-level theory."
        )
    }

    selected_style = style_guides.get(state.get("style", "ELI5"))

    # The rest of your chain remains the same
    prompt = ChatPromptTemplate.from_messages([
            ("system", f"You are a specialized Data Science Writer. Style Guide: {selected_style}"),
            ("human", f"Transform this research into a newsletter about {state['topic']}:\n\n{state['research_data']}")
        ])
    
    try:
        response = llm.invoke(prompt.format(data=state['research_data']))
        return {"newsletter_draft": response.content}
    except Exception as e:
        # If the guardrail triggers a block, handle it gracefully
        return {"newsletter_draft": "Content blocked by safety guardrails.", "steps_taken": ["blocked"]}