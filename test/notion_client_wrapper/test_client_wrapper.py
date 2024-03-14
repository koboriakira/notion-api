from unittest import TestCase

from notion_api.domain.database_type import DatabaseType
from notion_api.notion_client_wrapper.client_wrapper import ClientWrapper
from notion_api.notion_client_wrapper.properties.properties import Url


class TestClientWrapper(TestCase):
    def setUp(self):
        self.suite = ClientWrapper.get_instance()

    def test_1つの条件で絞り込む(self):
        # Given
        url = Url(value="https://open.spotify.com/track/6tPlPsvzSM74vRVn9O5v9K")

        # 音楽のページを取得してみる
        data = self.suite.retrieve_database(
            database_id=DatabaseType.MUSIC.value,
            properties=[url],
        )
        print(data)
        self.assertEqual(1, len(data["results"]))
