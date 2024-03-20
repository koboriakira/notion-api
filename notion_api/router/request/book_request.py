
from pydantic import BaseModel


class AddBookRequest(BaseModel):
    google_book_id: str | None = None
    title: str | None = None
    isbn: str | None = None
