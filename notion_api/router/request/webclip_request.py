from pydantic import BaseModel
from typing import Optional

class AddWebclipPageRequest(BaseModel):
    url: str
    title: str
    cover: Optional[str] = None
    slack_channel: Optional[str] = None
    slack_thread_ts: Optional[str] = None
