from typing import TypedDict, List

class NewsletterState(TypedDict):
    topic: str
    style: str  # Options: "academic", "ELI5", "tutorial"
    research_data: str
    newsletter_draft: str
    steps_taken: List[str]