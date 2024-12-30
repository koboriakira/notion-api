from unittest import TestCase

import pytest
from notion_api.infrastructure.book.google_book_api import GoogleBookApi
from requests import HTTPError

from book.book_api import NotFoundApiError


class TestGoogleBookApi(TestCase):
    def setUp(self):
        self.suite = GoogleBookApi()

    @pytest.mark.slow()
    def test_タイトルから本を検索できる(self):
        # Given
        title = "科学的根拠に基づく最高の勉強法"

        # When
        actual = self.suite.find_by_title(title=title)

        # Then
        self.assertEqual(actual.title, title)

    @pytest.mark.slow()
    def test_書籍名の検索結果がないとき(self):
        # pipenv run pytest test/infrastructure/book/test_google_book_api.py -k test_書籍名の検索結果がないとき

        # Given
        title = "ｄｊｆｄｌｓｊｆｌｓｄｌｄんｋｌ３えおうおふぃｈｄｆｈｓｄｆｓｄｆ；ｄｓｊｆっｓｄ"
        # When, Then: 例外が発生する
        with pytest.raises(NotFoundApiError):
            _ = self.suite.find_by_title(title=title)

    @pytest.mark.slow()
    def test_Google書籍IDの検索結果がないとき(self):
        # pipenv run pytest test/infrastructure/book/test_google_book_api.py -k test_Google書籍IDの検索結果がないとき

        # Given
        book_id = "hoge"
        # When, Then: 例外が発生する
        with pytest.raises(HTTPError):
            _ = self.suite.find_by_id(book_id=book_id)

    @pytest.mark.slow()
    def test_ISBNから本を検索できる(self):
        # Given
        isbn = "4314010746"
        title = "正義論"

        # When
        actual = self.suite.find_by_isbn(isbn=isbn)

        # Then
        self.assertEqual(actual.title, title)
