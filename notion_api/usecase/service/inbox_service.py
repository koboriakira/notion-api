
import os

from slack_sdk.web import WebClient

from domain.database_type import DatabaseType
from notion_client_wrapper.block.paragraph import Paragraph
from notion_client_wrapper.client_wrapper import ClientWrapper
from notion_client_wrapper.properties import Title


class InboxService:
    def __init__(
            self,
            slack_client: WebClient|None = None,
            client: ClientWrapper|None = None) -> None:
        self.client = client or ClientWrapper.get_instance()
        self.slack_client = slack_client or WebClient(token=os.environ["SLACK_BOT_TOKEN"])

    def add_inbox_task_by_page_id(  # noqa: PLR0913
            self,
            page_id: str, # NotionのページID
            page_url: str, # NotionのページURL
            original_url: str = "", # オリジナルのURL
            slack_channel: str | None = None,
            slack_thread_ts: str | None = None) -> None:
        """ Notionの他ページに関連するタスクを追加する """
        title = Title.from_mentioned_page_id(name="名前", page_id=page_id)
        inbox_task_page = self.client.create_page_in_database(
            database_id=DatabaseType.TASK.value,
            properties=[title])
        if original_url:
            paragraph = Paragraph.from_plain_text(text=original_url)
            self.client.append_block(block_id=inbox_task_page["id"], block=paragraph)
        if slack_channel is not None:
            self.slack_client.chat_postMessage(
                channel=slack_channel,
                text=f"ページを作成しました: {page_url}",
                thread_ts=slack_thread_ts,
            )
