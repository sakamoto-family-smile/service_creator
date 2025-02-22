from langchain_core.tools import Tool, BaseTool
from langchain.agents import load_tools
from langchain_google_community import GoogleSearchAPIWrapper


def google_search_tool() -> Tool:
    search = GoogleSearchAPIWrapper()
    return Tool(
        name="google_search",
        description="Search Google for recent results.",
        func=search.run,
    )


def human_feedback_tool() -> BaseTool:
    tools = load_tools(["human"])
    return tools[0]
