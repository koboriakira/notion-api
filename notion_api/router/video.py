from fastapi import APIRouter, Header
from typing import Optional
from interface import video
from util.access_token import valid_access_token
from router.response import BaseResponse
from router.request import AddVideoRequest
from custom_logger import get_logger
from interface import sqs

logger = get_logger(__name__)

router = APIRouter()


@router.post("", response_model=BaseResponse)
def add_video_page(request: AddVideoRequest,
                   access_token: Optional[str] = Header(None),
                ):
    valid_access_token(access_token)
    logger.debug(request)
    sqs.create_page(
        mode="video",
        params={
            "url": request.url,
            "title": request.title,
            "tags": request.tags,
            "cover": request.cover,
            "slack_channel": request.slack_channel,
            "slack_thread_ts": request.slack_thread_ts,
        }
    )
    return BaseResponse()
