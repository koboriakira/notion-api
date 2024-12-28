from lotion import Lotion

from custom_logger import get_logger
from infrastructure.book.google_book_api import GoogleBookApi
from usecase.add_book_usecase import AddBookUsecase

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
    client = Lotion.get_instance()
    usecase = AddBookUsecase(book_api=book_api, lotion=client)
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
