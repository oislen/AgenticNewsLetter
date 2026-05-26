import logging
from langchain_tavily import TavilySearch
from langchain_tavily._utilities import TavilySearchAPIWrapper
from langchain_core.runnables import RunnableConfig

from state import NewsletterState

def researcher_node(state: NewsletterState, config: RunnableConfig):
    """
    This node performs research on the specified topic and subtopic using the Tavily Search API. It constructs a search query based on the topic and subtopic, invokes the Tavily Search API to retrieve relevant information, and formats the results into a structured context that can be used by subsequent nodes in the newsletter generation process.

    Parameters
    ----------
    state : NewsletterState
        The current state of the newsletter generation process, which includes the topic and subtopic for research.
    config : RunnableConfig
        The configuration object that contains any necessary parameters for the researcher node, such as API keys for the Tavily Search API.

    Returns
    --------
    dict
        A dictionary containing the collated research data and the steps taken by the researcher node.
    """
    logging.info("Starting researcher node ...")
    # extract configurable parameters
    configurable = config.get("configurable", {})
    logging.info("Initiating Tavily ...")
    # initiate tavily search
    search = TavilySearch(
        max_results=5,
        search_depth="advanced",
        topic="news",
        api_wrapper=TavilySearchAPIWrapper(tavily_api_key=configurable.get("TAVILY_API_KEY"))
    )
    # define search query
    # We bias toward substantive, recent signal: research findings, notable
    # releases, new tools/libraries, and real-world applications — rather
    # than generic "news", which tends to surface shallow coverage.
    query = (
        f"recent significant developments in {state['subtopic']} "
        f"({state['topic']}): research breakthroughs, notable releases, "
        f"new tools or libraries, and real-world applications from the "
        f"last few weeks"
    )
    # perform search and format results
    search_results = search.invoke({"query": query})
    context = "\n".join([f"Title: {result['title']}\nURL: {result['url']}\nContent: {result['content']}\n---" for result in search_results['results']])
    logging.info("Collated research data from Tavily Search API.")
    return {"research_data": context, "steps_taken": ["researcher_complete"]}