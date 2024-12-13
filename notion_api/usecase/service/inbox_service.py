import os

from lotion import Lotion
from lotion.base_page import BasePage
from lotion.block import Bookmark, Embed
from lotion.properties import Title
from slack_sdk.web import WebClient

from common.value.database_type import DatabaseType
from music.domain.song import Song
from restaurant.domain.restaurant import Restaurant
from task.domain.memo_genre import MemoGenreKind, MemoGenreType
from video.domain.video import Video
from webclip.domain.webclip import Webclip


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
        title = Title.from_mentioned_page(
            mentioned_page_id=page.page_id,
            mentioned_page_title=page.title,
        )
        properties.append(title)
        memo_genre_kind = self.get_memo_genre_kind(page)
        if memo_genre_kind is not None:
            properties.append(memo_genre_kind)

        # タスクを作成
        inbox_task_page = self.client.create_page_in_database(
            database_id=DatabaseType.TASK.value,
            properties=properties,
        )

        # URL情報があれば追加
        if original_url:
            block = (
                Embed.from_url_and_caption(url=original_url)
                if isinstance(page, Song) or isinstance(page, Video)
                else Bookmark.from_url(url=original_url)
            )
            self.client.append_block(block_id=inbox_task_page.page_id.value, block=block)

        # Slackに通知
        if slack_channel is not None:
            self.slack_client.chat_postMessage(
                channel=slack_channel,
                text=f"ページを作成しました: {page.url}",
                thread_ts=slack_thread_ts,
            )

    def get_memo_genre_kind(self, page: BasePage) -> MemoGenreKind | None:
        """ページの種類を取得する"""
        if isinstance(page, Song):
            return MemoGenreKind(MemoGenreType.MUSIC)
        if isinstance(page, Video):
            return MemoGenreKind(MemoGenreType.VIDEO)
        if isinstance(page, Webclip):
            return MemoGenreKind(MemoGenreType.WEBCLIP)
        if isinstance(page, Restaurant):
            return MemoGenreKind(MemoGenreType.RESTAURANT)
        return None
