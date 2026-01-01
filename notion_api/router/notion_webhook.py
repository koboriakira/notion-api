import logging
from enum import StrEnum

from fastapi import APIRouter
from lotion import BasePage, Lotion
from pydantic import BaseModel

from book.book_openbd_api import BookOpenbdApi
from infrastructure.slack_bot_client import SlackBotClient
from injector.injector import Injector
from notion_databases.todo import Todo
from router.response import BaseResponse
from util.error_reporter import ErrorReporter

router = APIRouter()


class NotionWebhookType(StrEnum):
    SYNC_BOOK_INFO = "sync_book_info"
    # タスク関連のWebhook
    ABORT_TASK = "abort_task"  # タスクを中断 (「あとで」)
    START_TASK = "start_task"  # タスクを開始
    POSTPONE_TOMORROW = "postpone_tomorrow"  # タスクを翌日に延期
    CONVERT_TO_PROJECT = "convert_to_project"  # プロジェクトに変換
    COMPLETE_TASK = "complete_task"  # タスクを完了
    # 汎用性のあるWebhook
    CREATE_PROJECT = "create_project"  # 対象のページをタイトルにしたプロジェクトを作成


class NotionWebhookRequest(BaseModel):
    source: dict
    data: dict


@router.post("/{path}/")
def post_path(path: str, request: NotionWebhookRequest) -> BaseResponse:  # noqa: C901
    try:
        print("notion_webhook: post_path")
        logging.debug("notion_webhook: post_path")
        logging.info("notion_webhook: post_path")
        webhook_type = NotionWebhookType(path)
        base_page = BasePage.from_data(request.data)

        if webhook_type == NotionWebhookType.SYNC_BOOK_INFO:
            add_book_usecase = Injector.add_book_usecase(book_api=BookOpenbdApi())
            isbn = base_page.get_text("ISBN").text
            _ = add_book_usecase.execute(
                isbn=isbn,
                page_id=base_page.id,
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
            client = Lotion.get_instance()
            todo = client.retrieve_page(page_id=base_page.id, cls=Todo).inprogress()
            client.update(todo)
            return BaseResponse()
        if webhook_type == NotionWebhookType.POSTPONE_TOMORROW:
            task_util_service = Injector.task_util_serivce()
            task_util_service.postpone(page_id=base_page.id, days=1)
            return BaseResponse()
        if webhook_type == NotionWebhookType.COMPLETE_TASK:
            client = Lotion.get_instance()
            todo = client.retrieve_page(page_id=base_page.id, cls=Todo).complete()
            client.update(todo)
            return BaseResponse()
        if webhook_type == NotionWebhookType.CREATE_PROJECT:
            create_project_service = Injector.create_project_service()
            create_project_service.execute(relation_page_id=base_page.id)
            return BaseResponse()

        msg = f"指定されたWebhookが見つかりませんでした。path: {path}"
        raise ValueError(msg)
    except Exception as e:
        ErrorReporter().execute("notion_webhook: post_path", error=e)
        return BaseResponse(message="Error", data=e)


def get_webhook_type(path: str) -> NotionWebhookType:
    try:
        return NotionWebhookType(path)
    except:
        msg = f"指定されたWebhookが見つかりませんでした。path: {path}"
        slack_client = SlackBotClient()
        slack_client.send_message(channel="D0572EG3TN3", text=msg)
        raise ValueError(msg)
