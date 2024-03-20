import os
from unittest import TestCase

import pytest
from notion_api.domain.database_type import DatabaseType
from notion_client import Client


class TestNotionClient(TestCase):
    def setUp(self):
        self.client = Client(auth=os.getenv("NOTION_SECRET"))

    @pytest.mark.skip()
    def test_find_page(self):
        spotify_url = "https://open.spotify.com/track/6tPlPsvzSM74vRVn9O5v9K"
        # 音楽のページを取得してみる
        data = self.client.databases.query(
                database_id=DatabaseType.MUSIC.value,
                filter={
                    "property": "Spotify",
                    "url": {
                        "equals": spotify_url
                    }
                })
        print(data)
        self.assertEqual(1, len(data["results"]))

    @pytest.mark.learning()
    def test_current_tasks(self):
        # 現在のタスクを取得してみる
        filter_param = {
            "and": [
                {
                    "property": "タスク種別",
                    "select": {"does_not_equal": "ゴミ箱"}
                },
                {
                    "property": "実施日",
                    "date": {"equals": "2024-03-15"}
                },
                {
                    "or": [
                        {
                            "property": "ステータス",
                            "status": {"equals": "InProgress"}
                        },
                        {
                            "property": "ステータス",
                            "status": {"equals": "ToDo"}
                        }
                    ]
                }
            ]
        }
        data = self.client.databases.query(
                database_id=DatabaseType.TASK.value,
                filter=filter_param)
        print(data)
