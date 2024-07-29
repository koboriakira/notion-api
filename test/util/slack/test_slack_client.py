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

    @pytest.mark.use_genuine_api()
    def test_文字列をファイルとしてアップロード(self):
        # pytest test/util/slack/test_slack_client.py::TestSlackClient::test_文字列をファイルとしてアップロード

        # モックを利用しない
        suite = SlackClient.bot(channel_type=ChannelType.TEST, thread_ts=None)

        # Given
        content = "# テスト\n\n## テスト2\n\n- テスト3\n- テスト4"

        # When
        suite.upload_as_file(filename="test.md", content=content)
