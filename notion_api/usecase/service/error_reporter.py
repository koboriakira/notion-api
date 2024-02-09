from typing import Optional
import sys
import traceback
from infrastructure.slack_bot_client import SlackBotClient

class ErrorReporter:
    def __init__(self):
        self.slack_bot_client = SlackBotClient()

    def report_error(self, err: Exception, channel: Optional[str] = None, thread_ts: Optional[str] = None):
        t, v, tb = sys.exc_info()
        formatted_exception = "\n".join(traceback.format_exception(t, v, tb))
        if channel is None:
            self.slack_bot_client.send_message(
                channel="error",
                text=f"エラーが発生しました: {formatted_exception}",
                thread_ts=thread_ts,
            )
        else:
            self.slack_bot_client.send_message(
                channel="C05H3USHAJU", # test channel
                text=f"エラーが発生しました: {formatted_exception}",
            )
