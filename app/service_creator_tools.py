from langchain_core.tools import Tool
from langchain_community.tools.human import HumanInputRun
from langchain.agents import load_tools
from langchain_google_community import GoogleSearchAPIWrapper


def google_search_tool() -> Tool:
    search = GoogleSearchAPIWrapper()
    return Tool(
        name="google_search",
        description="Search Google for recent results.",
        func=search.run,
    )


# TODO : 利用時にエラーになってしまう
def human_feedback_tool() -> Tool:
    tools = load_tools(["human"])
    tool = Tool(
        name=tools[0].name,
        description=tools[0].description,
        func=tools[0].run
    )
    HumanInputRun.model_rebuild()
    return tool
