from datetime import date, datetime
from typing import TypeVar

from lotion import Lotion
from lotion.base_page import BasePage
from lotion.block import Embed, Heading, Paragraph
from lotion.block.rich_text import RichTextBuilder
from lotion.filter import Builder, Cond

from common.infrastructure.twitter.lambda_twitter_api import LambdaTwitterApi
from common.service.image.external_image_service import ExternalImageService
from common.value.database_type import DatabaseType
from common.value.slack_channel_type import ChannelType
from custom_logger import get_logger
from daily_log.domain.daily_log_repository import DailyLogRepository
from music.domain.song import Song
from notion_databases.book import Book
from notion_databases.zettlekasten import Zettlekasten
from project.domain.project import Project
from recipe.domain.recipe import Recipe
from task.domain.task_kind import TaskKindType
from task.domain.task_repository import TaskRepository
from task.domain.task_status import TaskStatusType
from util.date_range import DateRange
from util.datetime import JST, jst_today
from util.slack.slack_client import SlackClient
from video.domain.video import Video
from webclip.domain.webclip import Webclip

logger = get_logger(__name__)


LOG_FORMAT_APPEND_PAGE = "ページを追加しました: %s"

T = TypeVar("T", bound=BasePage)


class CollectUpdatedPagesUsecase:
    def __init__(
        self,
        task_repository: TaskRepository,
        daily_log_repository: DailyLogRepository,
        is_debug: bool | None = None,
    ) -> None:
        self.client = Lotion.get_instance()
        channel_type = ChannelType.DIARY if not is_debug else ChannelType.TEST
        self._slack_client = SlackClient.bot(channel_type=channel_type, thread_ts=None)
        self._task_repository = task_repository
        self._daily_log_repository = daily_log_repository
        self._twitter_api = LambdaTwitterApi()
        self.is_debug = is_debug

    def execute(self, date_range: DateRange) -> str:
        """
        指定された日付のデイリーログに、指定されたカテゴリの最新ページを追加する

        Args:
            target_datetime (datetime, optional):
                時刻。この時刻の24時間以内に更新されたページを取得する。
                指定しない場合は現在時刻を使用する。

        Returns:
            str: マークダウンテキスト
        """
        target_date = jst_today(is_previous_day_until_2am=True)
        # ブログ用のマークダウンテキスト
        markdown_text = f"""---
title:
date: {target_date.isoformat()}
tags: []
---
"""

        # デイリーログを取得
        daily_log_id = "dummy" if self.is_debug else self._proc_daily_log(target_date=target_date)

        # 今日完了したタスクを集める
        markdown_text += "\n"
        markdown_text += self._proc_tasks(date_range=date_range, daily_log_id=daily_log_id)

        # Zettlekastenを集める
        markdown_text += "\n"
        markdown_text += self._proc_zettlekastens(date_range=date_range, daily_log_id=daily_log_id)

        # レシピを集める
        markdown_text += "\n"
        markdown_text += self._proc_recipes(date_range=date_range, daily_log_id=daily_log_id)

        # プロジェクトを集める
        markdown_text += "\n"
        markdown_text += self._proc_projects(date_range=date_range, daily_log_id=daily_log_id)

        # 書籍を集める
        markdown_text += "\n"
        markdown_text += self._proc_books(date_range=date_range, daily_log_id=daily_log_id)

        # Webクリップを集める
        markdown_text += "\n"
        markdown_text += self._proc_webclips(date_range=date_range, daily_log_id=daily_log_id)

        # 今日見た動画を集める
        markdown_text += "\n"
        markdown_text += self._proc_videos(date_range=date_range, daily_log_id=daily_log_id)

        # 今日聴いた音楽を集める
        markdown_text += "\n"
        markdown_text += self._proc_songs(date_range=date_range, daily_log_id=daily_log_id)

        # 今日のTwitterを集める
        markdown_text += "\n"
        markdown_text += self._proc_twitter(date_range=date_range, daily_log_id=daily_log_id)

        # 今日アップした画像を集める
        markdown_text += "\n"
        markdown_text += self._proc_images(date_range=date_range)

        # マークダウンをファイルとしてSlackにアップロード
        filename = f"daily_log_{target_date.isoformat()}.md"
        self._slack_client.upload_as_file(filename=filename, content=markdown_text)

        return markdown_text

    def _proc_daily_log(self, target_date: date) -> str:
        """デイリーログを取得する。デイリーログのページIDを返す。"""
        daily_log = self._daily_log_repository.find(date=target_date)
        if not daily_log or not daily_log.id:
            msg = "デイリーログが見つかりません。"
            raise ValueError(msg)

        self._slack_client.chat_postMessage(
            text=f"デイリーログにサマリを追加します。\n{daily_log.url}",
            new_thread=True,
        )
        return daily_log.id

    def _proc_tasks(self, date_range: DateRange, daily_log_id: str) -> str:
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
        if not self.is_debug:
            self._append_heading(block_id=daily_log_id, title="今日完了したタスク")
        markdown_text = "\n## 今日完了したタスク\n"
        for done_task in done_tasks:
            if not self.is_debug:
                self._append_backlink(block_id=daily_log_id, page=done_task)
            markdown_text += f"\n- {done_task.get_title_text()}"
        return markdown_text

    def _proc_books(self, date_range: DateRange, daily_log_id: str) -> str:
        """書籍を処理する"""
        books = self._search(date_range, Book)

        if len(books) == 0:
            return ""

        if not self.is_debug:
            self._append_heading(block_id=daily_log_id, title="今日の書籍")
        markdown_text = "## 今日の書籍\n"
        for book in books:
            if not self.is_debug:
                self._append_backlink(block_id=daily_log_id, page=book)
            markdown_text += f"\n{book.get_title_text()}\n"
        return markdown_text

    def _proc_zettlekastens(self, date_range: DateRange, daily_log_id: str) -> str:
        """Zettlekastenを処理する"""
        zettlekastens = self._search(date_range, Zettlekasten)

        if len(zettlekastens) == 0:
            return ""

        if not self.is_debug:
            self._append_heading(block_id=daily_log_id, title="今日のZettlekasten")
        markdown_text = "## 今日のZettlekasten\n"
        for zettlekasten in zettlekastens:
            if not self.is_debug:
                self._append_backlink(block_id=daily_log_id, page=zettlekasten)
            markdown_text += f"\n{zettlekasten.get_title_text()}\n"
        return markdown_text

    def _proc_recipes(self, date_range: DateRange, daily_log_id: str) -> str:
        """レシピを処理する"""
        recipes = self._search(date_range, Recipe)

        if len(recipes) == 0:
            return ""

        if not self.is_debug:
            self._append_heading(block_id=daily_log_id, title="今日のレシピ")
        markdown_text = "## 今日のレシピ\n"
        for recipe in recipes:
            if not self.is_debug:
                self._append_backlink(block_id=daily_log_id, page=recipe)
            markdown_text += f"\n{recipe.get_title_text()}\n"
        return markdown_text

    def _proc_projects(self, date_range: DateRange, daily_log_id: str) -> str:
        """Projectを処理する"""
        projects = self._search(date_range, Project)

        if len(projects) == 0:
            return ""

        if not self.is_debug:
            self._append_heading(block_id=daily_log_id, title="今日のプロジェクト")
        markdown_text = "## 今日のプロジェクト\n"
        for project in projects:
            if not self.is_debug:
                self._append_backlink(block_id=daily_log_id, page=project)
            markdown_text += f"\n{project.get_title_text()}\n"
        return markdown_text

    def _proc_webclips(self, date_range: DateRange, daily_log_id: str) -> str:
        """WebClipを処理する"""
        webclips = self._search(date_range, Webclip)

        if len(webclips) == 0:
            return ""

        if not self.is_debug:
            self._append_heading(block_id=daily_log_id, title="今日のWebクリップ")
        markdown_text = "## 今日のWebクリップ\n"
        for webclip in webclips:
            if not self.is_debug:
                self._append_backlink(block_id=daily_log_id, page=webclip)
            markdown_text += f"\n[{webclip.get_title_text()}]({webclip.cliped_url})\n"
        return markdown_text

    def _proc_songs(self, date_range: DateRange, daily_log_id: str) -> str:
        songs = self._search(date_range, Song)
        if len(songs) == 0:
            return ""

        if not self.is_debug:
            self._append_heading(block_id=daily_log_id, title="今日聴いた音楽")
        markdown_text = "## 今日聴いた音楽\n"
        for song in songs:
            if not self.is_debug:
                self._append_backlink(block_id=daily_log_id, page=song)
            markdown_text += f"\n{song.artist} - {song.get_title_text()}\n"
            markdown_text += f"\n{song.embed_html}\n"
        return markdown_text

    def _proc_videos(self, date_range: DateRange, daily_log_id: str) -> str:
        videos = self._search(date_range, Video)
        if len(videos) == 0:
            return ""

        if not self.is_debug:
            self._append_heading(block_id=daily_log_id, title="今日見た動画")
        markdown_text = "## 今日見た動画\n"
        for video in videos:
            if not self.is_debug:
                self._append_backlink(block_id=daily_log_id, page=video)
            markdown_text += f"\n[{video.get_title_text()}]({video.url.url})\n"
            markdown_text += f"\n{video.embed_youtube_url}\n"
        return markdown_text

    def _proc_images(self, date_range: DateRange) -> str:
        """画像を処理する"""
        external_image_service = ExternalImageService()
        image_urls = external_image_service.get_images(date_range)

        if len(image_urls) == 0:
            return ""

        markdown_text = "## 今日アップした画像\n"
        for url in image_urls:
            markdown_text += f"\n![]({url})\n"
        return markdown_text

    def _proc_twitter(self, date_range: DateRange, daily_log_id: str) -> str:  # noqa: C901
        # 今日のTwitterを集める
        try:
            tweets = self._twitter_api.get_user_tweets(
                user_screen_name="kobori_akira_pw",
                start_datetime=date_range.start.value,
                end_datetime=date_range.end.value,
            )
            if len(tweets) == 0:
                return ""

            if not self.is_debug:
                self._append_heading(block_id=daily_log_id, title="今日のTwitter")
            markdown_text = "## 今日のTwitter\n"
            for tweet in tweets:
                markdown_text += f"\n{tweet.text}"
                markdown_text += f"\n{tweet.embed_tweet_html}\n"
                embed_tweet = Embed.from_url_and_caption(url=tweet.url)
                if not self.is_debug:
                    self.client.append_block(block_id=daily_log_id, block=embed_tweet)
                self._slack_client.chat_postMessage(text=tweet.url)
            return markdown_text
        except Exception as e:
            logger.error(e)
            return f"※ 今日のTwitterの取得に失敗しました {e}\n"

    def _get_latest_items(self, date_range: DateRange, database_type: DatabaseType) -> list[BasePage]:
        """指定されたカテゴリの、最近更新されたページIDを取得する"""
        builder = (
            Builder.create()
            .add_last_edited_at(Cond.ON_OR_AFTER, date_range.start.value.isoformat())
            .add_last_edited_at(Cond.ON_OR_BEFORE, date_range.end.value.isoformat())
        )
        filter_param = builder.build()
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
        heading = Heading.from_plain_text(heading_size=2, text=title)
        if not self.is_debug:
            self.client.append_block(block_id=block_id, block=heading)

    def _append_backlink(self, block_id: str, page: BasePage) -> None:
        rich_text = RichTextBuilder.get_instance().add_page_mention(page_id=page.id).build()
        paragraph = Paragraph.from_rich_text(rich_text=rich_text)
        if not self.is_debug:
            self.client.append_block(
                block_id=block_id,
                block=paragraph,
            )
        logger.info(LOG_FORMAT_APPEND_PAGE, page.get_title().text)

    def _search(self, date_range: DateRange, cls: type[T]) -> list[T]:
        builder = (
            Builder.create()
            .add_last_edited_at(Cond.ON_OR_AFTER, date_range.start.value.isoformat())
            .add_last_edited_at(
                Cond.ON_OR_BEFORE,
                date_range.end.value.isoformat(),
            )
        )
        return self.client.retrieve_pages(
            cls=cls,
            filter_param=builder.build(),
        )


if __name__ == "__main__":
    # python -m notion_api.usecase.collect_updated_pages_usecase
    from daily_log.infrastructure.daily_log_repository_impl import DailyLogRepositoryImpl
    from task.infrastructure.task_repository_impl import TaskRepositoryImpl

    client = Lotion.get_instance()
    task_repository = TaskRepositoryImpl(notion_client_wrapper=client)
    daily_log_repository = DailyLogRepositoryImpl(client=client)

    usecase = CollectUpdatedPagesUsecase(
        is_debug=True,
        task_repository=task_repository,
        daily_log_repository=daily_log_repository,
    )
    date_range = DateRange.from_datetime(
        start=datetime(2024, 12, 14, 0, 0, 0, tzinfo=JST),
        end=datetime(2024, 12, 16, 0, 0, 0, tzinfo=JST),
    )
    # print(usecase.execute(date_range=date_range))
    # print(usecase._proc_daily_log(target_date=date_range.end.value.date()))
    # print(usecase._proc_videos(date_range=date_range, daily_log_id="dummy"))
    # print(usecase._proc_images(date_range=date_range))
    # print(usecase._proc_projects(date_range=date_range, daily_log_id="dummy"))
    # print(usecase._proc_zettlekastens(date_range=date_range, daily_log_id="dummy"))
    print(usecase._proc_books(date_range=date_range, daily_log_id="dummy"))
    # print(usecase._proc_tasks(date_range=date_range, daily_log_id="dummy"))
