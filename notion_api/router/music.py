from fastapi import APIRouter, Header
from typing import Optional
from datetime import date as Date
from interface import music
from util.access_token import valid_access_token
from router.response import BaseResponse
from router.request import AddTrackPageRequest
from custom_logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.post("", response_model=BaseResponse)
def add_track_page(request: AddTrackPageRequest,
                   access_token: Optional[str] = Header(None),
                ):
    valid_access_token(access_token)
    logger.debug(request)
    release_date = Date.fromisoformat(request.release_date) if request.release_date else None
    result = music.add_track_page(
        track_name=request.track_name,
        artists=request.artists,
        spotify_url=request.spotify_url,
        cover_url=request.cover_url,
        release_date=release_date,
    )
    return BaseResponse(data=result)
