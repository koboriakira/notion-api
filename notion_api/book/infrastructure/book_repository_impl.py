from logging import Logger, getLogger

from lotion import Lotion
from lotion.base_page import BasePage

from book.domain.book import Book
from book.domain.book_repository import BookRepository, ExistedBookError, NotFoundBookError
from common.value.database_type import DatabaseType

DATABASE_ID = DatabaseType.BOOK.value


class BookRepositoryImpl(BookRepository):
    def __init__(self, client: Lotion, logger: Logger | None = None) -> None:
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
            page_id=result.page_id.value,
            url=result.url,
        )
        return book

    def __find_by_title(self, title: str) -> Book | None:
        base_page = self._client.find_page_by_title(
            database_id=DATABASE_ID,
            title=title,
            title_key_name="Title",
        )
        if base_page is None:
            return None
        return self._cast(base_page)

    def _cast(self, base_page: BasePage) -> Book:
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
