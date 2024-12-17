from dataclasses import dataclass
from datetime import date

from book.domain.authors import Authors
from book.domain.book_url import BookUrl
from book.domain.published_date import PublishedDate
from book.domain.publisher import Publisher
from lotion.base_page import BasePage
from lotion.page.page_id import PageId


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
