import os

from slack_sdk.web import WebClient

from common.value.database_type import DatabaseType
from music.domain.song import Song
from notion_client_wrapper.base_page import BasePage
from notion_client_wrapper.block.bookmark import Bookmark
from notion_client_wrapper.block.embed import Embed
from notion_client_wrapper.client_wrapper import ClientWrapper
from notion_client_wrapper.properties import Title
from video.domain.video import Video


class InboxService:
    def __init__(self, slack_client: WebClient | None = None, client: ClientWrapper | None = None) -> None:
        self.client = client or ClientWrapper.get_instance()
        self.slack_client = slack_client or WebClient(token=os.environ["SLACK_BOT_TOKEN"])

    def add_inbox_task_by_page_id(
        self,
        page: BasePage,
        original_url: str = "",  # オリジナルのURL
        slack_channel: str | None = None,
        slack_thread_ts: str | None = None,
    ) -> None:
        """Notionの他ページに関連するタスクを追加する"""
        kind_prefix = self.get_kind_prefix(page)
        title = Title.from_mentioned_page(
            mentioned_page_id=page.page_id,
            mentioned_page_title=page.title,
            prefix=kind_prefix,
        )
        inbox_task_page = self.client.create_page_in_database(database_id=DatabaseType.TASK.value, properties=[title])
        if original_url:
            block = (
                Embed.from_url_and_caption(url=original_url)
                if isinstance(page, Song) or isinstance(page, Video)
                else Bookmark.from_url(url=original_url)
            )
            self.client.append_block(block_id=inbox_task_page["id"], block=block)
        if slack_channel is not None:
            self.slack_client.chat_postMessage(
                channel=slack_channel,
                text=f"ページを作成しました: {page.url}",
                thread_ts=slack_thread_ts,
            )

    def get_kind_prefix(self, page: BasePage) -> str:
        """ページの種類を取得する"""
        if isinstance(page, Song):
            return "【音楽】"
        return "【未指定】"
