from typing import TypedDict, List

class NewsletterState(TypedDict):
    topic: str
    subtopic: str
    style: str
    research_data: str
    newsletter_draft: str
    steps_taken: List[str]
    bedrock_client: object