from pydantic import BaseModel
from typing import Optional

class AddVideoRequest(BaseModel):
    url: str
    title: str
    tags: list[str]
    cover: Optional[str] = None
