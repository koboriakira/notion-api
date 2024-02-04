from fastapi import APIRouter, Header
from typing import Optional
from util.access_token import valid_access_token
from router.response import BaseResponse
from custom_logger import get_logger
from router.request import AddBookRequest
from interface import book

logger = get_logger(__name__)

router = APIRouter()


@router.post("/regist", response_model=BaseResponse)
def add_track_page(request: AddBookRequest,
                   access_token: Optional[str] = Header(None),
                ):
    valid_access_token(access_token)
    result = book.add_book_by_google_book_id(id=request.google_book_id, title=request.title)
    return BaseResponse(data=result)
