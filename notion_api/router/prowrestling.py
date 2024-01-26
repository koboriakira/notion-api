from fastapi import APIRouter, Header
from typing import Optional
from interface import prowrestling
from util.access_token import valid_access_token
from router.response import BaseResponse
from router.request import AddProwrestlingRequest
from custom_logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.post("", response_model=BaseResponse)
def add_prowrestling_page(request: AddProwrestlingRequest,
                   access_token: Optional[str] = Header(None),
                ):
    valid_access_token(access_token)
    result = prowrestling.add_page(
        url=request.url,
        title=request.title,
        date=request.date,
        promotion=request.promotion,
        tags=request.tags,
        cover=request.cover,
    )
    return BaseResponse(data=result)
