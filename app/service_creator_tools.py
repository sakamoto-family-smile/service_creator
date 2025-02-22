from langchain_core.tools import Tool
from langchain_google_community import GoogleSearchAPIWrapper


def google_search_tool() -> Tool:
    search = GoogleSearchAPIWrapper()
    return Tool(
        name="google_search",
        description="Search Google for recent results.",
        func=search.run,
    )
