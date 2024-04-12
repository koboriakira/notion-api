from logging import Logger, getLogger

from book.domain.book import Book
from book.domain.book_repository import BookRepository, ExistedBookError, NotFoundBookError
from notion_client_wrapper.client_wrapper import ClientWrapper
from notion_client_wrapper.database.database_type import DatabaseType

DATABASE_ID = DatabaseType.BOOK.value


class BookRepositoryImpl(BookRepository):
    def __init__(self, client: ClientWrapper, logger: Logger | None = None) -> None:
        self._client = client
        self._logger = logger or getLogger(__name__)

    def find_by_title(self, title: str) -> Book | None:
        book = self.__find_by_title(title)
        if book is None:
            raise NotFoundBookError(title)
        return book

    def save(self, book: Book) -> Book:
        if self.__find_by_title(book.title) is None:
            raise ExistedBookError(book.title)
        result = self._client.create_page_in_database(
            database_id=DATABASE_ID,
            properties=book.properties.values,
            blocks=book.block_children,
            cover=book.cover,
        )
        book.update_id_and_url(
            page_id=result["id"],
            url=result["url"],
        )
        return book

    def __find_by_title(self, title: str) -> Book | None:
        return self._client.find_page_by_title(
            database_id=DATABASE_ID,
            title=title,
            title_key_name="Title",
            page_model=Book,
        )
