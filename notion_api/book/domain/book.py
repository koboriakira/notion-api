from dataclasses import dataclass
from datetime import date

from book.domain.authors import Authors
from book.domain.book_api import BookApiResult
from book.domain.book_title import BookTitle
from book.domain.book_url import BookUrl
from book.domain.published_date import PublishedDate
from book.domain.publisher import Publisher
from notion_client_wrapper.base_page import BasePage
from notion_client_wrapper.page.page_id import PageId
from notion_client_wrapper.properties.cover import Cover
from notion_client_wrapper.properties.properties import Properties


@dataclass
class Book(BasePage):
    @staticmethod
    def from_api_result(result: BookApiResult, author_page_id_list: list[PageId] | None) -> "Book":  # noqa: C901
        properties = [
            BookTitle(text=result.title),
        ]
        if author_page_id_list and len(author_page_id_list) > 0:
            authors = Authors.from_id_list(id_list=author_page_id_list)
            properties.append(authors)
        if result.publisher:
            publisher = Publisher.create(text=result.publisher)
            properties.append(publisher)
        if result.published_date:
            published_date = PublishedDate.create(result.published_date)
            properties.append(published_date)
        if result.url:
            url = BookUrl(result.url)
            properties.append(url)
        if result.image_url:
            cover = Cover.from_external_url(external_url=result.image_url)
            return Book(properties=Properties(properties), block_children=[], cover=cover)
        return Book(properties=Properties(properties), block_children=[])

    @property
    def author_page_id_list(self) -> list[PageId]:
        author = self.get_relation(name=Authors.NAME)
        return author.page_id_list if author else []

    @property
    def publisher(self) -> str:
        return self.get_text(name=Publisher.NAME).text

    @property
    def published_date(self) -> date | None:
        date_ = self.get_date(name=PublishedDate.NAME)
        return date_.start_date if date_ else None

    @property
    def book_url(self) -> str:
        url = self.get_url(name=BookUrl.NAME)
        return url.url if url else ""
