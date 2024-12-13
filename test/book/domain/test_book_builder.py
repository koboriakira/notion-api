from datetime import date
from unittest import TestCase
from unittest.mock import Mock

from lotion.page import PageId
from notion_api.book.domain.book_api import BookApiResult
from notion_api.book.domain.book_builder import BookBuilder
from notion_api.common.service.tag_creator.tag_creator import TagCreator


class TestBookBuilder(TestCase):
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
        # タグページを作成するサービスは使用しないためモックにする
        tag_creator = Mock(spec=TagCreator)
        author_page_id = PageId.dummy()
        tag_creator.execute.return_value = [author_page_id]

        # When
        book = BookBuilder.from_api_result(result=api_result, tag_creator=tag_creator)

        # Then
        self.assertEqual(book.get_title_text(), "Pythonの教科書")
        self.assertEqual(book.publisher, "株式会社A")
        self.assertEqual(book.published_date, date.fromisoformat("2022-01-01"))
        self.assertEqual(book.book_url, "https://example.com")
        self.assertEqual(book.cover.external_url, "https://example.com/image")
