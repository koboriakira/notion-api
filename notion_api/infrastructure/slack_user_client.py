import json
import os

from slack_sdk import WebClient

from domain.infrastructure.slack_client import SlackClient


class SlackUserClient(SlackClient):
    def __init__(self):
        self.client = WebClient(token=os.environ["SLACK_USER_TOKEN"])

    def send_message(self, channel: str, text: str, blocks: list | None = None, thread_ts: str | None = None) -> dict:
        return self.client.chat_postMessage(channel=channel, text=text, blocks=blocks, thread_ts=thread_ts)

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

TEST = "C05H3USHAJU"

if __name__ == "__main__":
    # python -m infrastructure.slack_user_client
    client = SlackUserClient()
    response = client.send_message(channel=TEST, text="test")
    ts = response["ts"]
    client.update_message(channel=TEST, ts=ts, text="test2")
