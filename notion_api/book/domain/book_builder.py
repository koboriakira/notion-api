from dataclasses import dataclass
from datetime import date

from lotion.block import Block
from lotion.properties import Cover, Properties, Property

from book.domain.authors import Authors
from book.domain.book import Book
from book.domain.book_api import BookApiResult
from book.domain.book_title import BookTitle
from book.domain.book_url import BookUrl
from book.domain.published_date import PublishedDate
from book.domain.publisher import Publisher
from common.service.tag_creator.tag_creator import TagCreator


@dataclass
class BookBuilder:
    properties: list[Property]
    blocks: list[Block]
    cover: Cover | None

    @staticmethod
    def of(title: str) -> "BookBuilder":
        properties: list[Property] = [BookTitle(text=title)]
        return BookBuilder(properties=properties, blocks=[], cover=None)

    @staticmethod
    def from_api_result(result: BookApiResult, tag_creator: TagCreator | None = None) -> Book:
        builder = BookBuilder.of(title=result.title).add_authors(
            authors=result.authors,
            tag_creator=tag_creator,
        )
        builder = builder.add_publishers(publisher=result.publisher) if result.publisher else builder
        builder = builder.add_published_date(published_date=result.published_date) if result.published_date else builder
        builder = builder.add_book_url(url=result.url) if result.url else builder
        builder = builder.add_cover(image_url=result.image_url) if result.image_url else builder
        return builder.build()

    def build(self) -> Book:
        return Book(properties=Properties(self.properties), block_children=self.blocks, cover=self.cover)

    def add_authors(self, authors: list[str], tag_creator: TagCreator | None = None) -> "BookBuilder":
        if not authors:
            return self
        tag_creator = tag_creator or TagCreator()

        # 事前に著者のタグページを作成
        tag_page_ids = tag_creator.execute(tag=authors)

        self.properties.append(Authors.from_id_list(id_list=tag_page_ids))
        return self

    def add_publishers(self, publisher: str) -> "BookBuilder":
        self.properties.append(Publisher.create(text=publisher))
        return self

    def add_published_date(self, published_date: date) -> "BookBuilder":
        self.properties.append(PublishedDate.create(published_date))
        return self

    def add_book_url(self, url: str) -> "BookBuilder":
        self.properties.append(BookUrl(url))
        return self

    def add_cover(self, image_url: str) -> "BookBuilder":
        self.cover = Cover.from_external_url(external_url=image_url)
        return self
