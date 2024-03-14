import os
from unittest import TestCase

import pytest
from notion_api.domain.database_type import DatabaseType
from notion_client import Client


class TestNotionClient(TestCase):
    def setUp(self):
        self.client = Client(auth=os.getenv("NOTION_SECRET"))

    @pytest.mark.learning()
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
