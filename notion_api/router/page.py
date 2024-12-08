from fastapi import APIRouter, Header

from custom_logger import get_logger
from interface import page
from notion_client_wrapper.page.page_id import PageId
from router.request import AddFeelingRequest, AddPomodoroCountRequest, AppendTextBlockRequest, UpdateStatusRequest
from router.response import BaseResponse
from usecase.service.page_remover import PageRemover
from util.access_token import valid_access_token

logger = get_logger(__name__)

router = APIRouter()


@router.post("/feeling")
def append_feeling(
    request: AddFeelingRequest,
    access_token: str | None = Header(None),
) -> BaseResponse:
    valid_access_token(access_token)
    logger.debug(request)
    page.append_feeling(page_id=request.page_id, value=request.value)
    return BaseResponse()


@router.post("/pomodoro-count")
def add_pomodoro_count(request: AddPomodoroCountRequest, access_token: str | None = Header(None)) -> BaseResponse:
    valid_access_token(access_token)
    logger.debug(request)
    # 一応requestにカウントを入れているが、現状はただ+1するだけとする
    page.add_pomodoro_count(page_id=request.page_id)
    return BaseResponse()


@router.post("/status")
def update_status(request: UpdateStatusRequest, access_token: str | None = Header(None)) -> BaseResponse:
    valid_access_token(access_token)
    logger.debug(request)
    page.update_status(page_id=request.page_id, value=request.value)
    return BaseResponse()


@router.post("/block/text")
def append_text_block(request: AppendTextBlockRequest, access_token: str | None = Header(None)) -> BaseResponse:
    valid_access_token(access_token)
    logger.debug(request)
    page.append_text_block(page_id=request.page_id, value=request.value)
    return BaseResponse()


@router.delete("/{page_id}")
def remove_page(page_id: str, access_token: str | None = Header(None)) -> BaseResponse:
    valid_access_token(access_token)
    page_remover = PageRemover()
    page_remover.execute(page_id=PageId(value=page_id))
    return BaseResponse(data={"page_id": page_id})
