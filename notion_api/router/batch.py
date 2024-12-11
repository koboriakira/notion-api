from datetime import timedelta

from fastapi import APIRouter, Header

from injector.injector import Injector
from router.request.recipe_request import AddRecipeRequest
from router.response.base_response import BaseResponse
from util.access_token import valid_access_token
from util.datetime import jst_now

router = APIRouter()


@router.get("create_next_schedule")
def create_next_schedule(
    request: AddRecipeRequest,
    access_token: str | None = Header(None),
) -> BaseResponse:
    valid_access_token(access_token)
    create_routine_task_use_case = Injector.create_routine_task_use_case()
    sync_external_calendar_usecase = Injector.sync_external_calendar_usecase()

    target_date = jst_now()
    if target_date.hour >= 17:
        target_date = target_date + timedelta(days=1)
    create_routine_task_use_case.execute(date_=target_date.date())
    sync_external_calendar_usecase.execute(date_=target_date.date())
    return BaseResponse()
