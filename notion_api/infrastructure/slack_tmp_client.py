import json
import os

from slack_sdk import WebClient


class SlackTmpClient:
    def __init__(self, client: WebClient):
        self.client = client

    @staticmethod
    def get_user_client() -> "SlackTmpClient":
        return SlackTmpClient(client=WebClient(token=os.environ["SLACK_USER_TOKEN"]))

    @staticmethod
    def get_bot_client() -> "SlackTmpClient":
        return SlackTmpClient(client=WebClient(token=os.environ["SLACK_BOT_TOKEN"]))

    def send_message(
        self,
        channel: str,
        text: str,
        blocks: list|None = None,
        thread_ts: list|None = None,
        is_enabled_mention: bool|None = None,
    ) -> dict:
        text = f"<@U04PQMBCFNE> {text}" if is_enabled_mention else text
        return self.client.chat_postMessage(
            channel=channel, text=text, blocks=blocks, thread_ts=thread_ts,
        )

    def update_message(self, channel: str, ts: str, text: str, blocks: list | None = None) -> dict:
        return self.client.chat_update(channel=channel, ts=ts, text=text, blocks=blocks)

    def update_context(self, channel: str, ts: str, context: dict) -> dict:
        context_block = {
            "type": "context",
            "elements": [
                {
                    "type": "plain_text",
                    "text": json.dumps(context, ensure_ascii=False),
                },
            ],
        }
        return self.client.chat_update(channel=channel, ts=ts, blocks=[context_block])
