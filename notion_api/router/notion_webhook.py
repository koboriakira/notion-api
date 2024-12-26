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
    # タスク関連のWebhook
    ABORT_TASK = "abort_task"  # タスクを中断
    START_TASK = "start_task"  # タスクを開始
    CONVERT_TO_PROJECT = "convert_to_project"  # プロジェクトに変換


class NotionWebhookRequest(BaseModel):
    source: dict
    data: dict


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
        if webhook_type == NotionWebhookType.ABORT_TASK:
            abort_task_usecase = Injector.abort_task_usecase()
            abort_task_usecase.execute(page_id=base_page.id)
            return BaseResponse()
        if webhook_type == NotionWebhookType.CONVERT_TO_PROJECT:
            convert_to_project_usecase = Injector.convert_to_project_usecase()
            convert_to_project_usecase.execute(page_id=base_page.id, title=base_page.get_title())
            return BaseResponse()
        if webhook_type == NotionWebhookType.START_TASK:
            task_util_service = Injector.task_util_serivce()
            task_util_service.start(page_id=base_page.id)
            return BaseResponse()

        msg = f"指定されたWebhookが見つかりませんでした。path: {path}"
        raise ValueError(msg)
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
