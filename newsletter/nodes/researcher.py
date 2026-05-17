from langchain_tavily import TavilySearch
from langchain_tavily._utilities import TavilySearchAPIWrapper
from langchain_core.runnables import RunnableConfig

from state import NewsletterState

def researcher_node(state: NewsletterState, config: RunnableConfig):
    """
    """
    # extract configurable parameters
    configurable = config.get("configurable", {})
    # initiate tavily search
    search = TavilySearch(
        max_results=5,
        search_depth="advanced",
        topic="news",
        api_wrapper=TavilySearchAPIWrapper(tavily_api_key=configurable.get("TAVILY_API_KEY"))
    )
    # define search query
    query = f"latest breakthroughs and news in {state['topic']} - {state['subtopic']}"
    # perform search and format results
    search_results = search.invoke({"query": query})
    context = "\n".join([f"Title: {result['title']}\nURL: {result['url']}\nContent: {result['content']}\n---" for result in search_results['results']])
    return {"research_data": context, "steps_taken": ["researcher_complete"]}