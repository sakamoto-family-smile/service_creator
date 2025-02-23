from langchain_core.tools import Tool
from langchain_google_community import GoogleSearchAPIWrapper


def google_search_tool() -> Tool:
    search = GoogleSearchAPIWrapper()
    return Tool(
        name="google_search",
        description="Search Google for recent results.",
        func=search.run,
    )


def human_feedback_tool() -> Tool:
    name = "human"
    description = """
        You can ask a human for guidance when you think you got stuck or you are not sure what to do next.
        The input should be a question for the human.
    """

    def _print_func(text: str) -> None:
        print("\n")  # noqa: T201
        print("====== Question for Human ======\n")
        print(text)  # noqa: T201

    def _run(query: str) -> str:
        _print_func(query)
        return input()

    tool = Tool(
        name=name,
        description=description,
        func=_run
    )
    return tool
