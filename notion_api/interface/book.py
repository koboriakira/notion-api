from book.infrastructure.book_repository_impl import BookRepositoryImpl
from custom_logger import get_logger
from infrastructure.book.google_book_api import GoogleBookApi
from notion_client_wrapper.client_wrapper import ClientWrapper
from usecase.add_book_usecase import AddBookUsecase
from usecase.service.tag_create_service import TagCreateService

logger = get_logger(__name__)


def add_book_by_google_book_id(
    google_book_id: str | None = None,
    title: str | None = None,
    isbn: str | None = None,
    slack_channel: str | None = None,
    slack_thread_ts: str | None = None,
) -> dict:
    book_api = GoogleBookApi()
    logger = get_logger(__name__)
    client = ClientWrapper.get_instance()
    book_repository = BookRepositoryImpl(
        client=client,
        logger=logger,
    )
    tag_create_service = TagCreateService(client=client)
    usecase = AddBookUsecase(book_api=book_api, book_repository=book_repository, tag_create_service=tag_create_service)
    return usecase.execute(
        google_book_id=google_book_id,
        title=title,
        isbn=isbn,
        slack_channel=slack_channel,
        slack_thread_ts=slack_thread_ts,
    )


if __name__ == "__main__":
    # python -m notion_api.interface.book
    add_book_by_google_book_id(title="マイクロサービスアーキテクチャ 第2版")
