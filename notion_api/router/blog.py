import logging
from datetime import datetime

from fastapi import APIRouter

from injector.injector import Injector
from router.response import BaseResponse
from util.date_range import DateRange
from util.datetime import JST, jst_now
from util.dynamodb.dynamodb import DynamoDBClient

router = APIRouter()

KEY = "latest-datetime-getting-blog-template"


@router.get("/template/", response_model=BaseResponse)
def get_blog_template(last_execution_time: bool | None = None) -> BaseResponse:
    """
    ブログのテンプレート文章を返却する
    """
    dynamodb_client = DynamoDBClient("NotionApi-NotionTableF26AF3BC-4263X0XU1OXU")
    try:
        # start_str = dynamodb_client.find("key", KEY)["datetime"]
        # start = datetime.fromisoformat(start_str)
        start = datetime(2024, 11, 16, 2, 0, 0, 0, JST)
        now = jst_now()

        usecase = Injector.create_collect_updated_pages_usecase()
        markdown_text = usecase.execute(
            date_range=DateRange.from_datetime(start=start, end=now),
        )

        try:
            dynamodb_client.put({"key": KEY, "datetime": now.isoformat()})
        except Exception:  # noqa: BLE001
            markdown_text += "\n\n※ テンプレート取得日時の更新に失敗しました。"
        return BaseResponse(message=markdown_text)
    except Exception as e:  # noqa: BLE001
        logging.error(e)
        return BaseResponse(message=f"エラーが発生しました: {e}")
