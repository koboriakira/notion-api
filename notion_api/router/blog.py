from datetime import datetime, timedelta
from fastapi import APIRouter, Header
import logging
from injector.injector import Injector
from router.response import BaseResponse
from util.date_range import DateRange
from util.datetime import JST, jst_now
from util.dynamodb.dynamodb import DynamoDBClient

router = APIRouter()

KEY = 'latest-datetime-getting-blog-template'

@router.get("/template/", response_model=BaseResponse)
def get_blog_template(last_execution_time: bool | None = None) -> BaseResponse:
    """
    ブログのテンプレート文章を返却する
    """
    try:
        usecase = Injector.create_collect_updated_pages_usecase()
        now = datetime(year=2024, month=11, day=15, hour=0, minute=0, second=0, tzinfo=JST)
        start = now - timedelta(days=1)

        data_range = DateRange.from_datetime(start=start, end=now)
        markdown_text = "test" + str(last_execution_time)
        markdown_text = usecase.execute(data_range)
        dynamodb_client = DynamoDBClient('NotionApi-NotionTableF26AF3BC-4263X0XU1OXU')
        dynamodb_client.put({'key': KEY, 'datetime': now.isoformat()})
        return BaseResponse(message=markdown_text)
    except Exception as e:
        logging.error(e)
        return BaseResponse(message=f"エラーが発生しました: {e}")
