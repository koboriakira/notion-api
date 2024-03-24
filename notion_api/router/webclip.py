
from fastapi import APIRouter, Header

from custom_logger import get_logger
from interface import sqs
from router.request import AddWebclipPageRequest
from router.response import BaseResponse
from util.access_token import valid_access_token

logger = get_logger(__name__)

router = APIRouter()


@router.post("", response_model=BaseResponse)
def add_webclip_page(request: AddWebclipPageRequest,
                   access_token: str | None = Header(None),
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
        },
    )
    return BaseResponse()
