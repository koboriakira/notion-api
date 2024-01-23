from pydantic import BaseModel
from typing import Optional

class AddTrackPageRequest(BaseModel):
    track_name: str
    artists: list[str]
    spotify_url: Optional[str] = None
    cover_url: Optional[str] = None
    release_date: Optional[str] = None
