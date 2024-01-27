from fastapi import APIRouter, Header
from typing import Optional
from interface import page
from util.access_token import valid_access_token
from router.response import BaseResponse
from router.request import AddFeelingRequest, AddPomodoroCountRequest
from custom_logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.post("/feeling", response_model=BaseResponse)
def append_feeling(request: AddFeelingRequest,
                   access_token: Optional[str] = Header(None),
                ):
    valid_access_token(access_token)
    logger.debug(request)
    page.append_feeling(page_id=request.page_id,value=request.value)
    return BaseResponse()

@router.post("/pomodoro-count", response_model=BaseResponse)
def add_pomodoro_count(request: AddPomodoroCountRequest,
                       access_token: Optional[str] = Header(None),):
    valid_access_token(access_token)
    logger.debug(request)
    # 一応requestにカウントを入れているが、現状はただ+1するだけとする
    page.add_pomodoro_count(page_id=request.page_id)
    return BaseResponse()
