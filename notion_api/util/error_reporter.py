import os
import sys
import traceback

from slack_sdk.web import WebClient

from util.environment import Environment

DM_CHANNEL = Environment.get_dm_channel()

class ErrorReporter:
    def __init__(self, client: WebClient|None=None) -> None:
        self.client = client or WebClient(token=os.environ["SLACK_BOT_TOKEN"])

    def execute(
            self,
            message: str|None = None,
            slack_channel: str|None = None,
            slack_thread_ts: str|None = None) -> None:

        message = message or "something error"
        formatted_exception = _generate_formatted_exception()
        text=f"[Notion-API]\n{message}\n\n```\n{formatted_exception}\n```"

        self.client.chat_postMessage(
            text=text,
            channel=slack_channel or DM_CHANNEL,
            thread_ts=slack_thread_ts)

def _generate_formatted_exception() -> str:
    exc_info = sys.exc_info()
    t, v, tb = exc_info
    return "\n".join(traceback.format_exception(t, v, tb))
