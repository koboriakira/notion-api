from dataclasses import dataclass
from datetime import date

from lotion.base_page import BasePage
from lotion.page.page_id import PageId

from book.domain.authors import Authors
from book.domain.book_url import BookUrl
from book.domain.published_date import PublishedDate
from book.domain.publisher import Publisher


@dataclass
class Book(BasePage):
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

    @property
    def isbn(self) -> str:
        return self.get_text(name="ISBN").text

    @staticmethod
    def cast(base_page: BasePage) -> "Book":
        return Book(
            properties=base_page.properties,
            block_children=base_page.block_children,
            id_=base_page.id_,
            url=base_page.url,
            created_time=base_page.created_time,
            last_edited_time=base_page.last_edited_time,
            _created_by=base_page._created_by,
            _last_edited_by=base_page._last_edited_by,
            cover=base_page.cover,
            icon=base_page.icon,
            archived=base_page.archived,
            parent=base_page.parent,
        )
