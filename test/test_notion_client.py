import os
from unittest import TestCase

import pytest
from notion_api.domain.database_type import DatabaseType
from notion_client import Client


class TestNotionClient(TestCase):
    def setUp(self):
        self.client = Client(auth=os.getenv("NOTION_SECRET"))

    @pytest.mark.skip()
    def test_retrieve_page(self):
        # pipenv run pytest test/test_notion_client.py -k test_retrieve_page
        import json

        page_id = "5c38fd30714b4ce2bf2d25407f3cfc16"
        data = self.client.pages.retrieve(page_id=page_id)
        print(json.dumps(data, indent=2, ensure_ascii=False))

        blocks = self.client.blocks.children.list(block_id=page_id)
        print(json.dumps(blocks["results"], indent=2, ensure_ascii=False))
        self.fail("標準出力確認のためのエラー")

    @pytest.mark.skip()
    def test_database_query(self):
        spotify_url = "https://open.spotify.com/track/6tPlPsvzSM74vRVn9O5v9K"
        data = self.client.databases.query(
            database_id=DatabaseType.MUSIC.value, filter={"property": "Spotify", "url": {"equals": spotify_url}}
        )
        print(data)
        self.assertEqual(1, len(data["results"]))

    @pytest.mark.learning()
    def test_current_tasks(self):
        """現在のタスクを取得してみる"""
        # pytest test/test_notion_client.py -k test_current_tasks

        # test_client_wrapper.py::TestClientWrapper::test_現在のタスクを取得する と異なる結果が出たりするので注意。
        filter_param = {
            "and": [
                {"property": "タスク種別", "select": {"does_not_equal": "ゴミ箱"}},
                {"property": "実施日", "date": {"equals": "2024-03-20"}},
                {
                    "or": [
                        {"property": "ステータス", "status": {"equals": "ToDo"}},
                        {"property": "ステータス", "status": {"equals": "InProgress"}},
                    ]
                },
            ]
        }
        data = self.client.databases.query(database_id=DatabaseType.TASK.value, filter=filter_param)
        print(len(data))
        # self.fail()

    @pytest.mark.learning()
    def test_relation_filter(self):
        """リレーション系のフィルターを試す"""
        # pytest test/test_notion_client.py -k test_relation_filter

        filter_param = {"property": "プロジェクト", "relation": {"contains": "5673db2d520f48fbad6622a38cf2ecad"}}
        data = self.client.databases.query(database_id=DatabaseType.TASK.value, filter=filter_param)
        print(data["results"])
        # self.fail()
