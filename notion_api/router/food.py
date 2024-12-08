from fastapi import APIRouter, Header
from pydantic import BaseModel

from custom_logger import get_logger
from router.response import BaseResponse
from util.access_token import valid_access_token

logger = get_logger(__name__)

router = APIRouter()


class AddFoodRequest(BaseModel):
    title: str


@router.post("/")
def add_track_page(request: AddFoodRequest, access_token: str | None = Header(None)) -> BaseResponse:
    valid_access_token(access_token)
    print(request.title)
    return BaseResponse(data="test")
