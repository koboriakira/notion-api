from datetime import datetime, timedelta
from fastapi import APIRouter, Header
import logging
from injector.injector import Injector
from router.response import BaseResponse
from util.date_range import DateRange
from util.datetime import JST, jst_now

router = APIRouter()


@router.get("/template", response_model=BaseResponse)
def get_blog_template():
    """
    ブログのテンプレート文章を返却する
    """
    usecase = Injector.create_collect_updated_pages_usecase()
    now = datetime(2024, 11, 15, 1, 18, 0, 0, JST)
    start = datetime(2024, 11, 14, 0, 0, 0, 0, JST)

    data_range = DateRange.from_datetime(start=start, end=now)
    markdown_text = usecase.execute(data_range)
    return BaseResponse(message=markdown_text)
