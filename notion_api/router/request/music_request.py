
from pydantic import BaseModel


class AddTrackPageRequest(BaseModel):
    track_name: str
    artists: list[str]
    spotify_url: str | None = None
    cover_url: str | None = None
    release_date: str | None = None
    slack_channel: str | None = None
    slack_thread_ts: str | None = None
