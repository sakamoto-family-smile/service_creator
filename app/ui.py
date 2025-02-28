import chainlit as cl
from chainlit.types import ThreadDict
from requirement_definition_phase import RequirementDefinitionPhase


# phase
requirement_phase = RequirementDefinitionPhase()


@cl.on_chat_start
async def on_chat_start():
    # チャット開始時に要求書（csv）をアップロードしてもらうように促す
    files = None
    while files is None:
        files = await cl.AskFileMessage(
            content="作りたいWebサービスの要求書をcsvフォーマットでアップロードしてください", accept=["text/csv"]
        ).send()

    request_csv_path = files[0]
    result = requirement_phase.before_kickoff(
        inputs={"request_list_path": request_csv_path}
    )


@cl.on_message
def on_message(msg: cl.Message):
    pass


@cl.on_stop
def on_stop():
    pass


@cl.on_chat_end
def on_chat_end():
    pass


@cl.on_chat_resume
async def on_chat_resume(thread: ThreadDict):
    pass
