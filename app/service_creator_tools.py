from langchain_core.tools import Tool
from langchain_google_community import GoogleSearchAPIWrapper
import chainlit as cl
from chainlit import run_sync


def google_search_tool() -> Tool:
    search = GoogleSearchAPIWrapper()
    return Tool(
        name="google_search",
        description="Search Google for recent results.",
        func=search.run,
    )


def human_feedback_tool_with_terminal() -> Tool:
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


def human_feedback_tool_with_chainlit() -> Tool:
    name = "human"
    description = """
        You can ask a human for guidance when you think you got stuck or you are not sure what to do next.
        The input should be a question for the human.
    """

    def _ask_human(text: str) -> str:
        human_response = run_sync(cl.AskUserMessage(content=f"{text}", timeout=600).send())
        if human_response:
            return human_response["output"]
        else:
            run_sync(cl.Message(content="ユーザーから回答を得られませんでした。次の処理に移行します。").send())

    tool = Tool(
        name=name,
        description=description,
        func=_ask_human
    )
    return tool
