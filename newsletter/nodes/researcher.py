from langchain_tavily import TavilySearch
from langchain_core.runnables import RunnableConfig

from state import NewsletterState

def researcher_node(state: NewsletterState, config: RunnableConfig):
    search = TavilySearch(max_results=5, search_depth="advanced", topic="news")
    query = f"latest breakthroughs and news in {state['topic']} for April 2026"
    search_results = search.invoke({"query": query})
    context = "\n".join([f"Title: {result['title']}\nURL: {result['url']}\nContent: {result['content']}\n---" for result in search_results['results']])
    return {"research_data": context, "steps_taken": ["researcher_complete"]}