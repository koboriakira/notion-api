from datetime import date
from unittest import TestCase

from notion_api.book.domain.book import Book
from notion_api.book.domain.book_api import BookApiResult
from notion_api.notion_client_wrapper.page.page_id import PageId


class TestBook(TestCase):
    def test_API実行結果からインスタンスを生成する(self):
        # Given
        api_result = BookApiResult(
            title="Pythonの教科書",
            authors=["山田太郎"],
            publisher="株式会社A",
            published_date=date.fromisoformat("2022-01-01"),
            url="https://example.com",
            image_url="https://example.com/image",
        )
        authors_page_id_list = [PageId.dummy()]

        # When
        book = Book.from_api_result(result=api_result, author_page_id_list=authors_page_id_list)

        # Then
        self.assertEqual(book.get_title_text(), "Pythonの教科書")
        self.assertEqual(book.publisher, "株式会社A")
        self.assertEqual(book.published_date, date.fromisoformat("2022-01-01"))
        self.assertEqual(book.book_url, "https://example.com")
