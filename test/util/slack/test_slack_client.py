from unittest import TestCase

import pytest
from notion_api.common.value.slack_channel_type import ChannelType
from notion_api.util.slack.slack_client import SlackClient


class TestSlackClient(TestCase):
    @pytest.mark.use_genuine_api()
    def test(self):
        # モックを利用しない
        suite = SlackClient.bot(channel_type=ChannelType.TEST, thread_ts=None)

        # When
        suite.chat_postMessage("test")
        suite.chat_postMessage("test:スレッド返信")
        suite.chat_postMessage("test:あたらしいスレッド", new_thread=True)
