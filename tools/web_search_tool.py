import requests
from langchain_core.tools import tool

from config.settings import TAVILY_API_KEY, TAVILY_API_URL





@tool
def search_web(query: str) -> dict:
    """
    Search the web for current travel-related information.

    Use this tool when up-to-date information is needed, such as
    travel disruptions, current events, recent attractions, or
    other information that may have changed recently.

    Args:
        query: The search query.

    Returns:
        A dictionary containing web search results.
    """

    if not TAVILY_API_KEY:
        return {
            "found": False,
            "results": [],
            "message": "Tavily API key is not configured.",
        }

    payload = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "search_depth": "basic",
        "max_results": 5,
    }

    try:
        response = requests.post(
            TAVILY_API_URL,
            json=payload,
            timeout=30,
        )

        if response.status_code != 200:
            return {
                "found": False,
                "results": [],
                "message": "Web search failed.",
                "status_code": response.status_code,
            }

        data = response.json()
        search_results = data.get("results", [])

        if not search_results:
            return {
                "found": False,
                "results": [],
                "message": "No web search results were found.",
            }

        results = []

        for result in search_results:
            results.append(
                {
                    "title": result.get("title"),
                    "url": result.get("url"),
                    "content": result.get("content"),
                }
            )

        return {
            "found": True,
            "results": results,
            "message": f"Found {len(results)} web search results.",
        }

    except requests.RequestException as error:
        return {
            "found": False,
            "results": [],
            "message": f"Web search request failed: {error}",
        }