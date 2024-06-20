from fastapi import APIRouter, Header

from custom_logger import get_logger
from interface import sqs
from router.request import AddTrackPageRequest
from router.response import BaseResponse
from util.access_token import valid_access_token

logger = get_logger(__name__)

router = APIRouter()


@router.post("", response_model=BaseResponse)
def add_track_page(
    request: AddTrackPageRequest,
    access_token: str | None = Header(None),
) -> BaseResponse:
    valid_access_token(access_token)
    logger.debug(request)
    sqs.create_page(
        mode="music",
        params={
            "url": request.spotify_url,
            "title": request.track_name,
            "cover": request.cover_url,
            "params": {
                "artists": request.artists,
                "release_date": request.release_date,
            },
            "slack_channel": request.slack_channel,
            "slack_thread_ts": request.slack_thread_ts,
        },
    )
    return BaseResponse()
