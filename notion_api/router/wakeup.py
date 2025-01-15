from fastapi import APIRouter
from lotion import Lotion
from pydantic import BaseModel

from notion_databases.daily_log import Condition, ConditionMemo, DailyLog, DailyLogTitle
from router.response.base_response import BaseResponse
from util.datetime import jst_today

router = APIRouter()


class WakeupRequest(BaseModel):
    condition: int
    condition_memo: str = ""


@router.post("/")
def wakeup(request: WakeupRequest) -> BaseResponse:
    lotion = Lotion.get_instance()
    daily_log = lotion.find_page(DailyLog, DailyLogTitle.from_date(jst_today()))
    if daily_log is None:
        raise Exception("DailyLog not found")
    daily_log.set_prop(Condition.from_num(request.condition))
    daily_log.set_prop(ConditionMemo.from_plain_text(request.condition_memo))
    lotion.update(daily_log)
    return BaseResponse()
