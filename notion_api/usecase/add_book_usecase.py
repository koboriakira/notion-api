
from custom_logger import get_logger
from domain.book.author import Author
from domain.book.book import Book
from domain.book.book_api import BookApi
from domain.database_type import DatabaseType
from notion_client_wrapper.client_wrapper import ClientWrapper
from notion_client_wrapper.filter.condition.string_condition import StringCondition
from notion_client_wrapper.filter.filter_builder import FilterBuilder
from usecase.service.tag_create_service import TagCreateService

logger = get_logger(__name__)

class AddBookUsecase:
    def __init__(
            self,
            book_api:BookApi,
            client_wrapper: ClientWrapper|None = None,
            tag_create_service: TagCreateService|None = None) -> None:
        self.book_api = book_api
        self.client = client_wrapper or ClientWrapper.get_instance()
        self.tag_create_service = tag_create_service or TagCreateService()

    def _find_book(
            self,
            google_book_id: str | None = None,
            title: str | None = None,
            isbn: str | None = None) -> Book|None:
        if google_book_id is not None:
            return self.book_api.find_by_id(book_id=google_book_id)
        if isbn is not None:
            return self.book_api.find_by_isbn(isbn=isbn)
        return self.book_api.find_by_title(title=title)

    def execute(
            self,
            google_book_id: str | None = None,
            title: str | None = None,
            isbn: str | None = None) -> dict:
        book = self._find_book(google_book_id=google_book_id, title=title, isbn=isbn)

        # データベースの取得
        filter_param = FilterBuilder().add_condition(StringCondition.equal(book.title)).build()
        searched_books = self.client.retrieve_database(
            database_id=DatabaseType.BOOK.value,
            filter_param=filter_param,
        )
        if len(searched_books) > 0:
            logger.info("The book is already registered")
            book = searched_books[0]
            return {
                "id": book.id,
                "url": book.url,
            }
        logger.info("Create a book page")

        # 著者のタグページを作成
        tag_page_ids:list[str] = [self.tag_create_service.add_tag(name=author) for author in book.author.text_list]
        author = Author.create(id_list=tag_page_ids) if len(tag_page_ids) > 0 else None

        # 新しいページを作成
        properties = [p for p in [
            book.title,
            author,
            book.published_date,
            book.publisher,
            book.url,
        ] if p is not None]

        result = self.client.create_page_in_database(
            database_id=DatabaseType.BOOK.value,
            cover=book.cover,
            properties=properties,
        )
        return {
            "id": result["id"],
            "url": result["url"],
        }
