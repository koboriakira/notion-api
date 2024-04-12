from book.domain.book_api import BookApi, BookApiResult
from book.domain.book_builder import BookBuilder
from book.domain.book_repository import BookRepository, ExistedBookError
from usecase.service.inbox_service import InboxService


class AddBookUsecase:
    def __init__(
        self,
        book_api: BookApi,
        book_repository: BookRepository,
    ) -> None:
        self._book_api = book_api
        self._book_repository = book_repository
        self._inbox_service = InboxService()

    def execute(  # noqa: PLR0913
        self,
        google_book_id: str | None = None,
        title: str | None = None,
        isbn: str | None = None,
        slack_channel: str | None = None,
        slack_thread_ts: str | None = None,
    ) -> dict:
        try:
            # 書籍情報を取得
            book_api_result = self._find_book(google_book_id=google_book_id, title=title, isbn=isbn)

            # ページインスタンスを生成、保存
            book = BookBuilder.from_api_result(result=book_api_result)
            book = self._book_repository.save(book=book)
            # Inboxにタスクを追加
            self._inbox_service.add_inbox_task_by_page_id(
                page_id=book.id,
                page_url=book.url,
                original_url=book.book_url,
                slack_channel=slack_channel,
                slack_thread_ts=slack_thread_ts,
            )
            return book.get_id_and_url()
        except ExistedBookError:
            # すでに登録されている場合はそれを取得する
            book = self._book_repository.find_by_title(title=book.title)
            return book.get_id_and_url()

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
