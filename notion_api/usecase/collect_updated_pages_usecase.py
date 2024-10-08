from datetime import datetime

from common.infrastructure.twitter.lambda_twitter_api import LambdaTwitterApi
from common.value.database_type import DatabaseType
from common.value.slack_channel_type import ChannelType
from custom_logger import get_logger
from daily_log.domain.daily_log_repository import DailyLogRepository
from music.domain.song_repository import SongRepository
from notion_client_wrapper import block
from notion_client_wrapper.base_page import BasePage
from notion_client_wrapper.block.embed import Embed
from notion_client_wrapper.block.rich_text.rich_text_builder import RichTextBuilder
from notion_client_wrapper.client_wrapper import ClientWrapper
from notion_client_wrapper.filter.condition.date_condition import DateCondition
from notion_client_wrapper.filter.filter_builder import FilterBuilder
from notion_client_wrapper.properties.last_edited_time import LastEditedTime
from task.domain.task_kind import TaskKindType
from task.domain.task_repository import TaskRepository
from task.domain.task_status import TaskStatusType
from util.date_range import DateRange
from util.datetime import JST
from util.slack.slack_client import SlackClient

logger = get_logger(__name__)

DATABASE_DICT = {
    "今日更新したプロジェクト": DatabaseType.PROJECT,
    "今日更新したZettlekasten": DatabaseType.ZETTLEKASTEN,
    "今日読んだ・登録した書籍": DatabaseType.BOOK,
    "今日更新したwebclip": DatabaseType.WEBCLIP,
    "今日観たプロレス": DatabaseType.PROWRESTLING,
    "今日更新・登録したレシピ": DatabaseType.RECIPE,
    "今日観た動画": DatabaseType.VIDEO,
    "今日聴いた音楽": DatabaseType.MUSIC,
}

LOG_FORMAT_APPEND_PAGE = "ページを追加しました: %s"


class CollectUpdatedPagesUsecase:
    def __init__(
        self,
        task_repository: TaskRepository,
        song_repository: SongRepository,
        daily_log_repository: DailyLogRepository,
        is_debug: bool | None = None,
    ) -> None:
        self.client = ClientWrapper.get_instance()
        channel_type = ChannelType.DIARY if not is_debug else ChannelType.TEST
        self._slack_client = SlackClient.bot(channel_type=channel_type, thread_ts=None)
        self._task_repository = task_repository
        self._song_repository = song_repository
        self._daily_log_repository = daily_log_repository
        self._twitter_api = LambdaTwitterApi()
        self.is_debug = is_debug

    def execute(self, date_range: DateRange) -> None:
        """
        指定された日付のデイリーログに、指定されたカテゴリの最新ページを追加する

        Args:
            target_datetime (datetime, optional):
                時刻。この時刻の24時間以内に更新されたページを取得する。
                指定しない場合は現在時刻を使用する。
        """
        target_date = date_range.end.value.date()
        # ブログ用のマークダウンテキスト
        markdown_text = f"""---
title:
date: {target_date.isoformat()}
tags: []
---
"""

        # デイリーログを取得
        daily_log = self._daily_log_repository.find(date=target_date)
        if not daily_log or not daily_log.id:
            msg = "デイリーログが見つかりません。"
            raise ValueError(msg)

        self._slack_client.chat_postMessage(
            text=f"デイリーログにサマリを追加します。\n{daily_log.url}",
            new_thread=True,
        )

        # 今日完了したタスクを取得
        done_tasks = self._task_repository.search(
            status_list=[TaskStatusType.DONE],
            kind_type_list=[
                TaskKindType.DO_NOW,
                TaskKindType.WAIT,
                TaskKindType.NEXT_ACTION,
                TaskKindType.SOMEDAY_MAYBE,
                TaskKindType.SCHEDULE,
            ],
            start_datetime=date_range.start.value,
            start_datetime_end=date_range.end.value,
        )
        markdown_text += "\n## 今日完了したタスク\n"
        markdown_text += "\n".join([f"- {task.get_title_text()}" for task in done_tasks])
        self._append_relation_to_daily_log(daily_log_id=daily_log.id, title="今日完了したタスク", pages=done_tasks)

        # 各データベースの更新ページを取得
        for title, database_type in DATABASE_DICT.items():
            pages = self._get_latest_items(date_range=date_range, database_type=database_type)
            self._append_relation_to_daily_log(daily_log_id=daily_log.id, title=title, pages=pages)
            markdown_text += f"\n## {title}\n"
            markdown_text += "\n".join([f"- {page.get_title_text()}" for page in pages])

        # 今日聴いた音楽を集める
        songs = self._song_repository.search(date_range)
        if len(songs) > 0:
            if not self.is_debug:
                self._append_heading(block_id=daily_log.id, title="今日聴いた音楽")
            markdown_text += "\n## 今日聴いた音楽\n"
            for song in songs:
                if not self.is_debug:
                    self._append_backlink(block_id=daily_log.id, page=song)
                markdown_text += f"\n{song.artist} - {song.get_title_text()}\n"
                markdown_text += f"\n{song.embed_html}\n"

        # 今日のTwitterを集める
        tweets = self._twitter_api.get_user_tweets(
            user_screen_name="kobori_akira_pw",
            start_datetime=date_range.end.value,
        )
        if len(tweets) > 0:
            if not self.is_debug:
                self._append_heading(block_id=daily_log.id, title="今日のTwitter")
            markdown_text += "\n## 今日のTwitter\n"
            markdown_text += "\n\n".join([f"{tweet.data.embed_tweet_html}" for tweet in tweets])
        for tweet in tweets:
            embed_tweet = Embed.from_url_and_caption(url=tweet.data.url)
            if not self.is_debug:
                self.client.append_block(block_id=daily_log.id, block=embed_tweet)
            self._slack_client.chat_postMessage(text=tweet.data.url)

        # マークダウンをファイルとしてSlackにアップロード
        filename = f"daily_log_{target_date.isoformat()}.md"
        self._slack_client.upload_as_file(filename=filename, content=markdown_text)

    def _get_latest_items(self, date_range: DateRange, database_type: DatabaseType) -> list[BasePage]:
        """指定されたカテゴリの、最近更新されたページIDを取得する"""
        last_edited_time_start = LastEditedTime.create(value=date_range.start.value)
        last_edited_time_end = LastEditedTime.create(value=date_range.end.value)
        filter_builder = FilterBuilder()
        filter_builder = filter_builder.add_condition(DateCondition.on_or_after(last_edited_time_start))
        filter_builder = filter_builder.add_condition(DateCondition.on_or_before(last_edited_time_end))
        filter_param = filter_builder.build()
        return self.client.retrieve_database(database_id=database_type.value, filter_param=filter_param)

    def _append_relation_to_daily_log(self, daily_log_id: str, title: str, pages: list[BasePage]) -> None:
        if len(pages) == 0:
            return
        # 見出しタグをつける
        if not self.is_debug:
            self._append_heading(block_id=daily_log_id, title=title)

        # バックリンクを記録する
        for page in pages:
            if not self.is_debug:
                self._append_backlink(block_id=daily_log_id, page=page)
            self._slack_client.chat_postMessage(text=page.title_for_slack())

    def _append_heading(self, block_id: str, title: str) -> None:
        heading = block.Heading.from_plain_text(heading_size=2, text=title)
        if not self.is_debug:
            self.client.append_block(block_id=block_id, block=heading)

    def _append_backlink(self, block_id: str, page: BasePage) -> None:
        rich_text = RichTextBuilder.get_instance().add_page_mention(page_id=page.id).build()
        paragraph = block.Paragraph.from_rich_text(rich_text=rich_text)
        if not self.is_debug:
            self.client.append_block(
                block_id=block_id,
                block=paragraph,
            )
        logger.info(LOG_FORMAT_APPEND_PAGE, page.get_title().text)


if __name__ == "__main__":
    # python -m notion_api.usecase.collect_updated_pages_usecase
    from daily_log.infrastructure.daily_log_repository_impl import DailyLogRepositoryImpl
    from music.infrastructure.song_repository_impl import SongRepositoryImpl
    from task.infrastructure.task_repository_impl import TaskRepositoryImpl

    client = ClientWrapper.get_instance()
    task_repository = TaskRepositoryImpl(notion_client_wrapper=client)
    song_repository = SongRepositoryImpl(client=client)
    daily_log_repository = DailyLogRepositoryImpl(client=client)

    usecase = CollectUpdatedPagesUsecase(
        is_debug=True,
        task_repository=task_repository,
        song_repository=song_repository,
        daily_log_repository=daily_log_repository,
    )
    date_range = DateRange.from_datetime(
        start=datetime(2024, 7, 29, 21, 0, 0, tzinfo=JST),
        end=datetime(2024, 7, 30, 21, 0, 0, tzinfo=JST),
    )
    usecase.execute(date_range=date_range)
