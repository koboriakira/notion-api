from datetime import datetime as DateTime

from pydantic import BaseModel


class BaseNotionPageModel(BaseModel):
    id: str
    url: str
    title: str
    created_at: DateTime
    updated_at: DateTime
    text: str | None
