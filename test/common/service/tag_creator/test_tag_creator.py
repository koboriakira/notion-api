from unittest import TestCase
from unittest.mock import Mock

from notion_api.common.service.tag_creator.tag_creator import TagCreator
from notion_api.notion_client_wrapper.base_page import BasePage
from notion_api.notion_client_wrapper.client_wrapper import ClientWrapper
from notion_api.notion_client_wrapper.properties.properties import Properties


class TestTagCreator(TestCase):
    def setUp(self) -> None:
        self.mock_client = Mock(spec=ClientWrapper)
        self.suite = TagCreator(client=self.mock_client)
        return super().setUp()

    def test_新規タグを作成する(self):
        # Given
        name_list = ["aaa", "bbb", "aaa"]

        # 既存のNotionページが存在しないとする
        self.mock_client.retrieve_database.return_value = []
        # Notionページを作成したときの挙動を設定
        self.mock_client.create_page_in_database.side_effect = [
            {"id": "111"},
            {"id": "222"},
        ]

        # When
        actual = self.suite.execute(name_list)

        # Then
        self.assertEqual(2, len(actual.id_list))
        self.assertIn("111", actual.id_list)
        self.assertIn("222", actual.id_list)

    def test_既存のタグページがあるときは作成をスキップする(self):
        # Given
        name_list = ["aaa"]

        # 既存のNotionページが存在するとする
        existed_tags = [
            BasePage(properties=Properties([]), block_children=[], id="111")
        ]
        self.mock_client.retrieve_database.return_value = existed_tags

        # When
        actual = self.suite.execute(name_list)

        # Then
        self.mock_client.create_page_in_database.assert_not_called()
        self.assertEqual(1, len(actual.id_list))
        self.assertIn("111", actual.id_list)
