from pydantic import BaseModel
from typing import Optional

class AddWebclipPageRequest(BaseModel):
    url: str
    title: str
    summary: str
    tags: list[str]
    status: str = "Inbox"
    cover: Optional[str] = None
    text: Optional[str] = None
