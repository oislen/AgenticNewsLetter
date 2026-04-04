from langgraph.graph import StateGraph, END
from state import NewsletterState

from nodes import researcher_node, writer_node, publisher_node

builder = StateGraph(NewsletterState)
builder.add_node("researcher", researcher_node)
builder.add_node("writer", writer_node)
builder.add_node("publisher", publisher_node)

builder.set_entry_point("researcher")
builder.add_edge("researcher", "writer")
builder.add_edge("writer", "publisher")
builder.add_edge("publisher", END)

if __name__ == "__main__":
    graph = builder.compile()
    
    # Change 'style' here to switch the newsletter's behavior
    graph.invoke({
        "topic": "Reinforcement Learning from Human Feedback", 
        "style": "tutorial", # Try "academic" or "ELI5"
        "steps_taken": []
    })