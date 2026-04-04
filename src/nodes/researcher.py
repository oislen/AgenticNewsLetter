from langchain_tavily import TavilySearch

from state import NewsletterState

def researcher_node(state: NewsletterState):
    search = TavilySearch(max_results=5, search_depth="advanced", topic="news")
    query = f"latest breakthroughs and news in {state['topic']} for April 2026"
    results = search.invoke({"query": query})
    
    context = "\n".join([f"Title: {r['title']}\nURL: {r['url']}\nContent: {r['content']}\n---" for r in results])
    return {"research_data": context, "steps_taken": ["researcher_complete"]}