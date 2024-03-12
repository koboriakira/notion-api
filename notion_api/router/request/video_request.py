
from pydantic import BaseModel


class AddVideoRequest(BaseModel):
    url: str
    title: str
    cover: str | None = None
    slack_channel: str | None = None
    slack_thread_ts: str | None = None
