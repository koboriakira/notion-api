import os

from slack_sdk import WebClient
from slack_sdk.web import SlackResponse

from domain.infrastructure.slack_client import SlackClient


class SlackBotClient(SlackClient):
    def __init__(self) -> None:
        self.client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])

    def send_message(
        self,
        channel: str,
        text: str,
        blocks: list | None = None,
        thread_ts: str | None = None,
        is_enabled_mention: bool | None = None,
    ) -> SlackResponse:
        text = f"<@U04PQMBCFNE> {text}" if is_enabled_mention else text
        return self.client.chat_postMessage(
            channel=channel,
            text=text,
            blocks=blocks,
            thread_ts=thread_ts,
        )

    def update_message(
        self,
        channel: str,
        ts: str,
        text: str,
        blocks: list | None = None,
    ) -> SlackResponse:
        return self.client.chat_update(channel=channel, ts=ts, text=text, blocks=blocks)


TEST = "C05H3USHAJU"

if __name__ == "__main__":
    # python -m infrastructure.slack_bot_client
    client = SlackBotClient()
    response = client.send_message(channel=TEST, text="test")
    ts = response["ts"]
    client.update_message(channel=TEST, ts=ts, text="test2")
