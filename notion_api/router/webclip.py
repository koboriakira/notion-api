from fastapi import APIRouter, Header
from typing import Optional
from datetime import date as Date
from interface import sqs
from util.access_token import valid_access_token
from router.response import BaseResponse
from router.request import AddWebclipPageRequest
from custom_logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.post("", response_model=BaseResponse)
def add_webclip_page(request: AddWebclipPageRequest,
                   access_token: Optional[str] = Header(None),
                ):
    valid_access_token(access_token)
    logger.debug(request)
    sqs.create_page(
        mode="webclip",
        params={
            "url": request.url,
            "title": request.title,
            "cover": request.cover,
            "slack_channel": request.slack_channel,
            "slack_thread_ts": request.slack_thread_ts,
        }
    )
    return BaseResponse()
