from pydantic import BaseModel
from typing import Optional

class AddBookRequest(BaseModel):
    google_book_id: Optional[str] = None
    title: Optional[str] = None
