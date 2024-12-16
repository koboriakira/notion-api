from pydantic import BaseModel


class AddBookRequest(BaseModel):
    google_book_id: str | None = None
    title: str | None = None
    isbn: str | None = None
    slack_channel: str | None = None
    slack_thread_ts: str | None = None


class UpdatePageRequest(BaseModel):
    page_id: str
    isbn: str
