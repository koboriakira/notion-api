from fastapi import APIRouter, Header

from custom_logger import get_logger
from interface import book
from router.request import AddBookRequest
from router.request.book_request import UpdatePageRequest
from router.response import BaseResponse
from util.access_token import valid_access_token

logger = get_logger(__name__)

router = APIRouter()


@router.post("/regist")
def add_track_page(request: AddBookRequest, access_token: str | None = Header(None)) -> BaseResponse:
    valid_access_token(access_token)
    result = book.add_book_by_google_book_id(
        google_book_id=request.google_book_id,
        title=request.title,
        isbn=request.isbn,
        slack_channel=request.slack_channel,
        slack_thread_ts=request.slack_thread_ts,
    )
    return BaseResponse(data=result)


@router.post("/update_page/")
def update_page(request, access_token: str | None = Header(None)) -> BaseResponse:
    valid_access_token(access_token)
    print(request)
    # result = book.add_book_by_google_book_id(
    #     page_id=request.page_id,
    #     isbn=request.isbn,
    # )
    return BaseResponse()
