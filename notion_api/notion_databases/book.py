from lotion import notion_database, notion_prop
from lotion.base_page import BasePage
from lotion.properties import Date, Relation, Text, Title, Url

from common.value.database_type import DatabaseType


@notion_prop("著者")
class Author(Relation):
    pass


@notion_prop("名前")
class BookTitle(Title):
    pass


@notion_prop("URL")
class BookUrl(Url):
    pass


@notion_prop("出版日")
class PublishedDate(Date):
    pass


@notion_prop("出版社")
class Publisher(Text):
    pass


@notion_prop("ISBN")
class Isbn(Text):
    pass


@notion_database(DatabaseType.BOOK.value)
class Book(BasePage):
    title: BookTitle
    author: Author
    url: BookUrl
    published_date: PublishedDate
    publisher: Publisher
    isbn: Isbn

    def get_author_page_id_list(self) -> list[str]:
        return self.author.id_list
