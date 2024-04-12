from logging import Logger, getLogger

from book.domain.book import Book
from book.domain.book_repository import BookRepository
from book.domain.book_title import BookTitle
from notion_client_wrapper.client_wrapper import ClientWrapper
from notion_client_wrapper.database.database_type import DatabaseType
from notion_client_wrapper.filter.filter_builder import FilterBuilder

DATABASE_ID = DatabaseType.BOOK.value


class BookRepositoryImpl(BookRepository):
    def __init__(self, client: ClientWrapper, logger: Logger | None = None) -> None:
        self._client = client
        self._logger = logger or getLogger(__name__)

    def find_by_title(self, title: str) -> Book | None:
        title_property = BookTitle(text=title)
        filter_param = FilterBuilder.build_simple_equal_condition(title_property)
        searched_book = self._client.retrieve_database(
            database_id=DATABASE_ID,
            filter_param=filter_param,
            page_model=Book,
        )
        if len(searched_book) == 0:
            return None
        if len(searched_book) > 1:
            warning_message = f"Found multiple book with the same title: {title}"
            self._logger.warning(warning_message)
        return searched_book[0]

    def save(self, book: Book) -> Book:
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
