from fastapi import APIRouter, Header
from typing import Optional
from interface import page
from util.access_token import valid_access_token
from router.response import BaseResponse
from router.request import AddFeelingRequest
from custom_logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.post("/feeling", response_model=BaseResponse)
def add_webclip_page(request: AddFeelingRequest,
                   access_token: Optional[str] = Header(None),
                ):
    valid_access_token(access_token)
    logger.debug(request)
    page.append_feeling(page_id=request.page_id,value=request.value)
    return BaseResponse()
