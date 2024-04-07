import os
from dataclasses import dataclass

from slack_sdk import WebClient

from common.value.slack_channel_type import ChannelType


@dataclass(frozen=True)
class EventTs:
    value: str


class SlackClient:
    def __init__(self, web_client: WebClient, channel: str, thread_ts: str | None) -> None:
        self._web_client = web_client
        self._channel = channel
        self._thread_ts = thread_ts

    def chat_postMessage(self, text: str, new_thread: bool | None = None) -> None:
        """シンプルなメッセージの送信。これより複雑なものはSlackConciergeAPIに移行すること"""
        thread_ts = None if new_thread else self._thread_ts
        response = self._web_client.chat_postMessage(channel=self._channel, text=text, thread_ts=thread_ts)
        event_ts = response["ts"]
        # スレッドの最初の投稿になる場合は、以降がスレッド返信になるようにthread_tsを設定する
        if self._thread_ts is None:
            self._thread_ts = event_ts

    @staticmethod
    def bot(channel_type: ChannelType, thread_ts: str | None = None) -> "SlackClient":
        return SlackClient(
            web_client=WebClient(token=os.environ["SLACK_BOT_TOKEN"]),
            channel=channel_type.value,
            thread_ts=thread_ts,
        )


class MockSlackClient(SlackClient):
    def __init__(self) -> None:
        self.is_started_thread = False

    def chat_postMessage(self, text: str, new_thread: bool | None = None) -> None:
        if new_thread or not self.is_started_thread:
            print(f"{text}\n-------------------------")
            self.is_started_thread = True
        else:
            print(f"    {text}\n    -------------------------")
