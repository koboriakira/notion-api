from book.domain.book import Book
from book.domain.book_api import BookApi, BookApiResult
from book.domain.book_repository import BookRepository
from custom_logger import get_logger
from notion_client_wrapper.page.page_id import PageId
from usecase.service.inbox_service import InboxService
from usecase.service.tag_create_service import TagCreateService

logger = get_logger(__name__)


class AddBookUsecase:
    def __init__(
        self,
        book_api: BookApi,
        book_repository: BookRepository,
        tag_create_service: TagCreateService,
    ) -> None:
        self._book_api = book_api
        self._book_repository = book_repository
        self._tag_create_service = tag_create_service
        self._inbox_service = InboxService()

    def _find_book(
        self,
        google_book_id: str | None = None,
        title: str | None = None,
        isbn: str | None = None,
    ) -> BookApiResult | None:
        if google_book_id is not None:
            return self._book_api.find_by_id(book_id=google_book_id)
        if isbn is not None:
            return self._book_api.find_by_isbn(isbn=isbn)
        return self._book_api.find_by_title(title=title)

    def execute(
        self,
        google_book_id: str | None = None,
        title: str | None = None,
        isbn: str | None = None,
        slack_channel: str | None = None,
        slack_thread_ts: str | None = None,
    ) -> dict:
        book_api_result = self._find_book(google_book_id=google_book_id, title=title, isbn=isbn)

        # すでに登録されているか確認
        book = self._book_repository.find_by_title(title=book_api_result.title)
        if book is not None:
            return {
                "id": book.id,
                "url": book.url,
            }
        logger.info("Create a book page")

        # 先に著者のタグページを作成
        tag_page_ids = [self._tag_create_service.add_tag(name=author) for author in book_api_result.authors]

        # ページインスタンスを生成、保存
        book = Book.from_api_result(result=book_api_result, author_page_id_list=[PageId(id_) for id_ in tag_page_ids])
        book = self._book_repository.save(book=book)

        self._inbox_service.add_inbox_task_by_page_id(
            page_id=book.id,
            page_url=book.url,
            original_url=book.book_url,
            slack_channel=slack_channel,
            slack_thread_ts=slack_thread_ts,
        )

        return {
            "id": book.id,
            "url": book.url,
        }
