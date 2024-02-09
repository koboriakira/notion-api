from typing import Optional
from slack_sdk import WebClient
import os
from domain.infrastructure.slack_client import SlackClient

class SlackUserClient(SlackClient):
    def __init__(self):
        self.client = WebClient(token=os.environ["SLACK_USER_TOKEN"])

    def send_message(self, channel: str, text: str, blocks: Optional[list] = None, thread_ts: Optional[str] = None) -> dict:
        return self.client.chat_postMessage(channel=channel, text=text, blocks=blocks, thread_ts=thread_ts)

    def update_message(self, channel: str, ts: str, text: str, blocks: Optional[list] = None) -> dict:
        return self.client.chat_update(channel=channel, ts=ts, text=text, blocks=blocks)

TEST = "C05H3USHAJU"

if __name__ == "__main__":
    # python -m infrastructure.slack_user_client
    client = SlackUserClient()
    response = client.send_message(channel=TEST, text="test")
    ts = response["ts"]
    client.update_message(channel=TEST, ts=ts, text="test2")
