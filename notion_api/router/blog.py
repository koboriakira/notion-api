import logging
from datetime import datetime

from fastapi import APIRouter

from injector.injector import Injector
from router.response import BaseResponse
from util.date_range import DateRange
from util.datetime import jst_now
from util.dynamodb.dynamodb import DynamoDBClient

router = APIRouter()

KEY = "latest-datetime-getting-blog-template"
dynamodb_client = DynamoDBClient("NotionApi-NotionTableF26AF3BC-4263X0XU1OXU")


@router.get("/template/", response_model=BaseResponse)
def get_blog_template(last_execution_time: bool | None = None) -> BaseResponse:
    """
    ブログのテンプレート文章を返却する
    """
    try:
        start_str = dynamodb_client.find("key", KEY)["datetime"]
        start = datetime.fromisoformat(start_str)
        now = jst_now()

        usecase = Injector.create_collect_updated_pages_usecase()
        markdown_text = usecase.execute(
            date_range=DateRange.from_datetime(start=start, end=now),
        )

        dynamodb_client.put({"key": KEY, "datetime": now.isoformat()})
        return BaseResponse(message=markdown_text)
    except Exception as e:
        logging.error(e)
        return BaseResponse(message=f"エラーが発生しました: {e}")
