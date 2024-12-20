import json
import logging
from enum import StrEnum

from fastapi import APIRouter
from lotion import BasePage
from pydantic import BaseModel

from book.domain.book import Book
from infrastructure.slack_bot_client import SlackBotClient
from injector.injector import Injector
from router.response import BaseResponse

router = APIRouter()


class NotionWebhookType(StrEnum):
    SYNC_BOOK_INFO = "sync_book_info"


class NotionWebhookRequest(BaseModel):
    source: dict
    data: dict


@router.post("/")
def post(request: NotionWebhookRequest) -> BaseResponse:
    try:
        print("notion_webhook: post")
        logging.debug("notion_webhook: post")
        logging.info("notion_webhook: post")
        print(request)
        print(request.data)
        print(json.dumps(request.data, ensure_ascii=False))
        base_page = BasePage.from_data(request.data)
        print(base_page.id)
        return BaseResponse()
    except Exception as e:
        print(e)
        return BaseResponse(message="Error", data=e)


@router.post("/{path}/")
def post_path(path: str, request: NotionWebhookRequest) -> BaseResponse:
    try:
        print("notion_webhook: post_path")
        logging.debug("notion_webhook: post_path")
        logging.info("notion_webhook: post_path")
        webhook_type = NotionWebhookType(path)
        base_page = BasePage.from_data(request.data)
        if webhook_type == NotionWebhookType.SYNC_BOOK_INFO:
            add_book_usecase = Injector.add_book_usecase()
            book = Book.cast(base_page=base_page)
            _ = add_book_usecase.execute(
                isbn=book.isbn,
                page_id=book.id,
            )
        return BaseResponse()
    except Exception as e:
        print(e)
        return BaseResponse(message="Error", data=e)


def get_webhook_type(path: str) -> NotionWebhookType:
    try:
        return NotionWebhookType(path)
    except:
        msg = f"指定されたWebhookが見つかりませんでした。path: {path}"
        slack_client = SlackBotClient()
        slack_client.send_message(channel="D0572EG3TN3", text=msg)
        raise ValueError(msg)
