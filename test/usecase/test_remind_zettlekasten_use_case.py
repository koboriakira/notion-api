from datetime import datetime
from unittest import TestCase
from unittest.mock import Mock

from lotion import Lotion
from notion_api.usecase.remind_zettlekasten_use_case import RemindZettlekastenUseCase
from notion_databases.zettlekasten import Zettlekasten
from slack_sdk import WebClient


class TestRemindZettlekastenUseCase(TestCase):
    def setUp(self):
        mock_lotion = Mock(spec=Lotion)
        mock_slack_client = Mock(spec=WebClient)
        self.suite = RemindZettlekastenUseCase(lotion=mock_lotion, slack_client=mock_slack_client)

    def test_execute(self):
        # Given

        # 1つのZettlekastenを返す。作成済にしたいので作成日時を埋め込む
        mock_zettlekasten = Zettlekasten.generate(title="テスト")
        mock_zettlekasten.created_time = datetime.now()

        self.suite._lotion.retrieve_pages.return_value = [mock_zettlekasten]

        # When, Then: ふつうに実行ができれば終わり
        self.assertIsNone(self.suite.execute())
