from pydantic import BaseModel
from typing import Optional
from datetime import date as Date

class AddProwrestlingRequest(BaseModel):
    url: str
    title: str
    date: Date
    promotion: str
    text: Optional[str] = None
    tags: list[str] = []
    cover: Optional[str] = None
