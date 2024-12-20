from datetime import datetime
from unittest import TestCase
from unittest.mock import Mock

from notion_api.usecase.remind_zettlekasten_use_case import RemindZettlekastenUseCase
from notion_api.zettlekasten.domain.zettlekasten import Zettlekasten
from notion_api.zettlekasten.domain.zettlekasten_repository import ZettlekastenRepository
from slack_sdk import WebClient


class TestRemindZettlekastenUseCase(TestCase):
    def setUp(self):
        mock_zettlekasten_repository = Mock(spec=ZettlekastenRepository)
        mock_slack_client = Mock(spec=WebClient)
        self.suite = RemindZettlekastenUseCase(
            zettlekasten_repository=mock_zettlekasten_repository, slack_client=mock_slack_client
        )

    def test_execute(self):
        # Given

        # 1つのZettlekastenを返す。作成済にしたいので作成日時を埋め込む
        mock_zettlekasten = Zettlekasten.create(title="テスト")
        mock_zettlekasten.created_time = datetime.now()

        self.suite._zettlekasten_repository.fetch_all.return_value = [mock_zettlekasten]

        # When, Then: ふつうに実行ができれば終わり
        self.assertIsNone(self.suite.execute())
