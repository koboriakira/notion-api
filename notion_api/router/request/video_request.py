from pydantic import BaseModel
from typing import Optional

class AddVideoRequest(BaseModel):
    url: str
    title: str
    cover: Optional[str] = None
    slack_channel: Optional[str] = None
    slack_thread_ts: Optional[str] = None
