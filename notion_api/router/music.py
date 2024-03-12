from datetime import date

from fastapi import APIRouter, Header

from custom_logger import get_logger
from router.request import AddTrackPageRequest
from router.response import BaseResponse
from usecase.add_track_page_usecase import AddTrackPageUsecase
from util.access_token import valid_access_token

logger = get_logger(__name__)

router = APIRouter()


@router.post("", response_model=BaseResponse)
def add_track_page(request: AddTrackPageRequest,
                   access_token: str | None = Header(None),
                ) -> BaseResponse:
    valid_access_token(access_token)
    logger.debug(request)
    release_date = date.fromisoformat(request.release_date) if request.release_date else None
    usecase = AddTrackPageUsecase()
    usecase.execute(
        track_name=request.track_name,
        artists=request.artists,
        spotify_url=request.spotify_url,
        cover_url=request.cover_url,
        release_date=release_date,
        slack_channel=request.slack_channel,
        slack_thread_ts=request.slack_thread_ts,
    )
    return BaseResponse()
