from dataclasses import dataclass
from datetime import date

from domain.book.author import Author
from domain.book.published_date import PublishedDate
from domain.book.publisher import Publisher
from notion_client_wrapper.properties.cover import Cover
from notion_client_wrapper.properties.title import Title
from notion_client_wrapper.properties.url import Url


@dataclass
class Book:
    title: Title
    author: Author|None
    publisher: Publisher|None
    published_date: PublishedDate|None
    url: Url|None
    cover: Cover|None

    @staticmethod
    def create(  # noqa: PLR0913
            title: str,
            authors: list[str],
            publisher: str|None = None,
            published_date: date|None = None,
            image_url: str|None = None,
            url: str|None = None) -> "Book":
        return Book(
            title=Title.from_plain_text(name="Title", text=title),
            author=Author.create(text_list=authors) if authors is not None else None,
            publisher=Publisher.create(text=publisher) if publisher is not None else None,
            published_date=PublishedDate.create(start_date=published_date) if published_date is not None else None,
            url=Url.from_url(name="URL", url=url) if url is not None else None,
            cover=Cover.from_external_url(external_url=image_url) if image_url is not None else None,
        )
