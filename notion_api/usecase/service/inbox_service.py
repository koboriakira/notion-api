import os

from lotion import Lotion
from lotion.base_page import BasePage
from lotion.block import Bookmark, Embed
from lotion.properties import Title
from slack_sdk.web import WebClient

from notion_databases.restaurant import Restaurant
from notion_databases.song import Song
from notion_databases.task import MemoGenre, Task
from notion_databases.task_prop.memo_genre import MemoGenreType
from notion_databases.video import Video
from notion_databases.webclip import Webclip


class InboxService:
    def __init__(
        self,
        slack_client: WebClient | None = None,
        client: Lotion | None = None,
    ) -> None:
        self.client = client or Lotion.get_instance()
        self.slack_client = slack_client or WebClient(
            token=os.environ["SLACK_BOT_TOKEN"],
        )

    def add_inbox_task_by_page_id(
        self,
        page: BasePage,
        original_url: str = "",  # オリジナルのURL
        slack_channel: str | None = None,
        slack_thread_ts: str | None = None,
    ) -> None:
        """Notionの他ページに関連するタスクを追加する"""

        # タイトルとメモジャンルを取得
        properties = []
        properties.append(Title.from_mentioned_page(mentioned_page_id=page.id))

        if memo_genre_kind := self.get_memo_genre_kind(page):
            properties.append(memo_genre_kind)

        # タスクを作成
        inbox_task = self.client.update(Task.create(properties=properties))

        # URL情報があれば追加
        if original_url:
            block = (
                Embed.from_url_and_caption(url=original_url)
                if isinstance(page, Song | Video)
                else Bookmark.from_url(url=original_url)
            )
            self.client.append_block(block_id=inbox_task.id, block=block)

        # Slackに通知
        if slack_channel is not None:
            self.slack_client.chat_postMessage(
                channel=slack_channel,
                text=f"ページを作成しました: {page.url}",
                thread_ts=slack_thread_ts,
            )

    def get_memo_genre_kind(self, page: BasePage) -> MemoGenre | None:
        """ページの種類を取得する"""
        if isinstance(page, Song):
            return MemoGenre.create(MemoGenreType.MUSIC)
        if isinstance(page, Video):
            return MemoGenre.create(MemoGenreType.VIDEO)
        if isinstance(page, Webclip):
            return MemoGenre.create(MemoGenreType.WEBCLIP)
        if isinstance(page, Restaurant):
            return MemoGenre.create(MemoGenreType.RESTAURANT)
        return None
