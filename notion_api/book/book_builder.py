from dataclasses import dataclass
from datetime import date

from lotion.block import Block
from lotion.properties import Cover, Properties, Property

from book.book_api import BookApiResult
from common.service.tag_creator.tag_creator import TagCreator
from notion_databases.book import Author, Book, BookTitle, BookUrl, PublishedDate, Publisher


@dataclass
class BookBuilder:
    properties: list[Property]
    blocks: list[Block]
    cover: Cover | None

    @staticmethod
    def of(title: str) -> "BookBuilder":
        properties: list[Property] = [BookTitle.from_plain_text(text=title)]
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

        self.properties.append(Author.from_id_list(id_list=tag_page_ids))
        return self

    def add_publishers(self, publisher: str) -> "BookBuilder":
        self.properties.append(Publisher.from_plain_text(publisher))
        return self

    def add_published_date(self, published_date: date) -> "BookBuilder":
        self.properties.append(PublishedDate.from_start_date(published_date))
        return self

    def add_book_url(self, url: str) -> "BookBuilder":
        self.properties.append(BookUrl.from_url(url))
        return self

    def add_cover(self, image_url: str) -> "BookBuilder":
        self.cover = Cover.from_external_url(external_url=image_url)
        return self
