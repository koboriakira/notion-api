from fastapi import APIRouter, Header
from typing import Optional
from interface import video
from util.access_token import valid_access_token
from router.response import BaseResponse
from router.request import AddVideoRequest
from custom_logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.post("", response_model=BaseResponse)
def add_webclip_page(request: AddVideoRequest,
                   access_token: Optional[str] = Header(None),
                ):
    valid_access_token(access_token)
    logger.debug(request)
    result = video.add_page(
        url=request.url,
        title=request.title,
        tags=request.tags,
        cover=request.cover,
    )
    return BaseResponse(data=result)
