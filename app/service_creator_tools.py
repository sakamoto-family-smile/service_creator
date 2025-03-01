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


class HumanFeedbackTool:
    def __init__(self, ui_type: str = "web"):
        self.__ui_type = ui_type

    def get_human_feedback_tool(self, author: str) -> Tool:
        name = "human"
        description = """
            You can ask a human for guidance when you think you got stuck or you are not sure what to do next.
            The input should be a question for the human.
        """

        if self.__ui_type == "terminal":
            def _print_func(text: str) -> None:
                print("\n")  # noqa: T201
                print("====== Question for Human ======\n")
                print(text)  # noqa: T201

            def _func(text: str) -> str:
                _print_func(text)
                return input()
        elif self.__ui_type == "web":
            def _func(text: str) -> str:
                human_response = run_sync(cl.AskUserMessage(
                    content=f"{text}",
                    author=author,
                    timeout=600
                ).send())
                if human_response:
                    return human_response["output"]
                else:
                    run_sync(cl.Message(content="ユーザーから回答を得られませんでした。次の処理に移行します。").send())
        else:
            raise NotImplementedError(f"{self.__ui_type} is not implemented! ")

        return Tool(
            name=name,
            description=description,
            func=_func
        )
