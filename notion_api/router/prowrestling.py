
from fastapi import APIRouter, Header

from custom_logger import get_logger
from interface import prowrestling
from router.request import AddProwrestlingRequest
from router.response import BaseResponse
from util.access_token import valid_access_token

logger = get_logger(__name__)

router = APIRouter()


@router.post("", response_model=BaseResponse)
def add_prowrestling_page(request: AddProwrestlingRequest,
                   access_token: str | None = Header(None),
                ):
    valid_access_token(access_token)
    result = prowrestling.add_page(
        url=request.url,
        title=request.title,
        date=request.date,
        promotion=request.promotion,
        text=request.text,
        tags=request.tags,
        cover=request.cover,
    )
    return BaseResponse(data=result)
