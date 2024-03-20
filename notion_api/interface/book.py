

from custom_logger import get_logger
from infrastructure.book.google_book_api import GoogleBookApi
from usecase.add_book_usecase import AddBookUsecase

logger = get_logger(__name__)

def add_book_by_google_book_id(
        google_book_id: str | None = None,
        title: str | None = None,
        isbn: str | None = None,
        ) -> dict:
    book_api = GoogleBookApi()
    usecase = AddBookUsecase(book_api=book_api)
    return usecase.execute(google_book_id=google_book_id, title=title, isbn=isbn)
