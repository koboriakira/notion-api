from unittest import TestCase

import pytest
from notion_api.domain.database_type import DatabaseType
from notion_api.notion_client_wrapper.client_wrapper import ClientWrapper
from notion_api.notion_client_wrapper.properties.title import Title
from notion_api.notion_client_wrapper.properties.url import Url


class TestClientWrapper(TestCase):
    def setUp(self):
        self.suite = ClientWrapper.get_instance()

    @pytest.mark.use_genuine_api()
    def test_すべてのデータを取得できる(self):
        # 音楽のページを取得してみる
        pages = self.suite.retrieve_database(
            database_id=DatabaseType.BOOK.value,
        )
        self.assertTrue(len(pages) > 0)


    @pytest.mark.use_genuine_api()
    def test_1つの条件で絞り込む(self):
        # Given
        url = Url.from_url(name="Spotify", url="https://open.spotify.com/track/6tPlPsvzSM74vRVn9O5v9K")

        # 音楽のページを取得してみる
        pages = self.suite.retrieve_database(
            database_id=DatabaseType.MUSIC.value,
            properties=[url],
        )
        self.assertEqual(1, len(pages))
        self.assertEqual("タバコロード 20", pages[0].get_title().text)

    @pytest.mark.use_genuine_api()
    def test_タイトルを使って絞り込む_title引数(self):
        # Given
        title = "タバコロード 20"

        # 音楽のページを取得してみる
        pages = self.suite.retrieve_database(
            database_id=DatabaseType.MUSIC.value,
            title=title,
        )
        self.assertEqual(1, len(pages))
        self.assertEqual("タバコロード 20", pages[0].get_title().text)

    @pytest.mark.use_genuine_api()
    def test_タイトルを使って絞り込む_titleをpropertyで(self):
        # Given
        title = Title.from_plain_text(name="名前", text="タバコロード 20")

        # 音楽のページを取得してみる
        pages = self.suite.retrieve_database(
            database_id=DatabaseType.MUSIC.value,
            properties=[title],
        )
        self.assertEqual(1, len(pages))
        self.assertEqual("タバコロード 20", pages[0].get_title().text)
