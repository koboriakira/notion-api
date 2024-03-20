from unittest import TestCase

import pytest
from notion_api.infrastructure.book.google_book_api import GoogleBookApi


class TestGoogleBookApi(TestCase):
    def setUp(self):
        self.suite = GoogleBookApi()

    @pytest.mark.slow()
    def test_タイトルから本を検索できる(self):
        # Given
        title="科学的根拠に基づく最高の勉強法"

        # When
        actual = self.suite.find_by_title(title=title)

        # Then
        self.assertEqual(actual.title.text, title)

    @pytest.mark.slow()
    def test_検索結果がないとき(self):
        # Given
        title="ｄｊｆｄｌｓｊｆｌｓｄｌｄんｋｌ３えおうおふぃｈｄｆｈｓｄｆｓｄｆ；ｄｓｊｆっｓｄ"

        # When
        actual = self.suite.find_by_title(title=title)

        # Then
        self.assertIsNone(actual)

    @pytest.mark.slow()
    def test_ISBNから本を検索できる(self):
        # Given
        isbn="4314010746"
        title="正義論"

        # When
        actual = self.suite.find_by_isbn(isbn=isbn)

        # Then
        self.assertEqual(actual.title.text, title)
