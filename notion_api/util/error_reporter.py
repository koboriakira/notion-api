import os
import sys
import traceback

from slack_sdk.web import WebClient

from util.environment import Environment
from notion_client_wrapper.client_wrapper import NotionApiError

DM_CHANNEL = Environment.get_dm_channel()

ERROR_MESSAGE_PUBLIC_API_UNAVAILABLE = "Public API service is temporarily unavailable"


class ErrorReporter:
    def __init__(self, client: WebClient | None = None) -> None:
        self.client = client or WebClient(token=os.environ["SLACK_BOT_TOKEN"])

    def execute(
        self,
        message: str | None = None,
        slack_channel: str | None = None,
        slack_thread_ts: str | None = None,
        error: Exception | None = None,
    ) -> None:
        message = message or "something error"
        formatted_exception = _generate_formatted_exception()

        if Environment.is_dev():
            print(formatted_exception)
            return

        try:
            if isinstance(error, NotionApiError):
                # errorがNotionAPIErrorの場合、簡易なメッセージにする
                last_line = formatted_exception.split("\n")[-2]
                self.client.chat_postMessage(
                    text=f"[Notion-API]\nNotion側のエラー\n\n```\n{last_line}\n```",
                    channel=slack_channel or DM_CHANNEL,
                    thread_ts=slack_thread_ts,
                )
                return

            text = f"[Notion-API]\n{message}\n\n```\n{formatted_exception}\n```"
            self.client.chat_postMessage(
                text=text,
                channel=slack_channel or DM_CHANNEL,
                thread_ts=slack_thread_ts,
            )
        except:  # noqa: E722
            print("Failed to send a message to Slack")
            print(text)


def _generate_formatted_exception() -> str:
    exc_info = sys.exc_info()
    t, v, tb = exc_info
    return "\n".join(traceback.format_exception(t, v, tb))
