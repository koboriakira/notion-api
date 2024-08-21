from fastapi import APIRouter, Header

from injector.injector import Injector
from router.request.account_book_request import PostAccountBookRequest
from router.response.base_response import BaseResponse
from util.access_token import valid_access_token
from util.datetime import jst_today

router = APIRouter()


@router.post("/", response_model=BaseResponse)
def add(
    request: PostAccountBookRequest,
    access_token: str | None = Header(None),
) -> BaseResponse:
    valid_access_token(access_token)
    usecase = Injector.create_add_account_book_use_case()
    account_book = usecase.execute(
        title=request.title,
        price=request.price,
        is_fixed_cost=request.is_fixed_cost,
        category=request.category,
        tag=request.tag,
        date_=jst_today(),
    )
    return BaseResponse(data=account_book)
