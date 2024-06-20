import os
from datetime import datetime, timedelta

from slack_sdk.web import WebClient

from common.infrastructure.twitter.lambda_twitter_api import LambdaTwitterApi
from common.value.database_type import DatabaseType
from custom_logger import get_logger
from daily_log.domain.daily_log_repository import DailyLogRepository
from notion_client_wrapper import block
from notion_client_wrapper.base_page import BasePage
from notion_client_wrapper.block.embed import Embed
from notion_client_wrapper.block.rich_text.rich_text_builder import RichTextBuilder
from notion_client_wrapper.client_wrapper import ClientWrapper
from notion_client_wrapper.filter.condition.date_condition import DateCondition
from notion_client_wrapper.filter.filter_builder import FilterBuilder
from notion_client_wrapper.properties.last_edited_time import LastEditedTime
from task.domain.task_repository import TaskRepository
from task.domain.task_status import TaskStatusType
from util.datetime import JST, jst_now

logger = get_logger(__name__)

DATABASE_TYPE_DAILY_LOG = DatabaseType.DAILY_LOG

DATABASE_DICT = {
    # "今日更新したタスク": DatabaseType.TASK,
    # "今日更新したプロジェクト": DatabaseType.PROJECT,
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
        daily_log_repository: DailyLogRepository,
        is_debug: bool | None = None,
    ) -> None:
        self.client = ClientWrapper.get_instance()
        self._slack_client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])
        self._task_repository = task_repository
        self._daily_log_repository = daily_log_repository
        self._twitter_api = LambdaTwitterApi()
        self.is_debug = is_debug

    def execute(self, target_datetime: datetime | None = None) -> None:
        """
        指定された日付のデイリーログに、指定されたカテゴリの最新ページを追加する

        Args:
            target_datetime (datetime, optional):
                時刻。この時刻の24時間以内に更新されたページを取得する。
                指定しない場合は現在時刻を使用する。
        """
        # 初期値の整理
        target_datetime = target_datetime or jst_now()

        # デイリーログを取得
        daily_log = self._daily_log_repository.find(date=target_datetime.date())

        # 今日完了したタスクを取得
        done_tasks = self._task_repository.search(
            status_list=[TaskStatusType.DONE],
            start_datetime=target_datetime - timedelta(hours=24),
            start_datetime_end=target_datetime,
        )
        self._append_relation_to_daily_log(daily_log_id=daily_log.id, title="今日完了したタスク", pages=done_tasks)

        for title, database_type in DATABASE_DICT.items():
            pages = self._get_latest_items(target_datetime=target_datetime, database_type=database_type)
            self._append_relation_to_daily_log(daily_log_id=daily_log.id, title=title, pages=pages)

        # 今日のTwitterを集める
        tweets = self._twitter_api.get_user_tweets(user_screen_name="kobori_akira_pw", start_datetime=target_datetime)
        for tweet in tweets:
            embed_tweet = Embed.from_url_and_caption(url=tweet.data.url)
            self.client.append_block(block_id=daily_log.id, block=embed_tweet)

        self._slack_client.chat_postMessage(
            text=f"デイリーログにページを追加しました。\n{daily_log.url}",
            channel="C05F6AASERZ",  # diary
        )

    def _get_latest_items(self, target_datetime: datetime, database_type: DatabaseType) -> list[BasePage]:
        """指定されたカテゴリの、最近更新されたページIDを取得する"""
        start = target_datetime - timedelta(hours=24)
        last_edited_time_start = LastEditedTime.create(value=start)
        last_edited_time_end = LastEditedTime.create(value=target_datetime)

        filter_builder = FilterBuilder()
        filter_builder = filter_builder.add_condition(DateCondition.on_or_after(last_edited_time_start))
        filter_builder = filter_builder.add_condition(DateCondition.on_or_before(last_edited_time_end))
        filter_param = filter_builder.build()
        return self.client.retrieve_database(database_id=database_type.value, filter_param=filter_param)

    def _append_relation_to_daily_log(self, daily_log_id: str, title: str, pages: list[BasePage]) -> None:
        if len(pages) == 0:
            return
        # 見出しタグをつける
        self._append_heading(block_id=daily_log_id, title=title)

        # バックリンクを記録する
        for page in pages:
            self._append_backlink(block_id=daily_log_id, page=page)

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
    from task.infrastructure.task_repository_impl import TaskRepositoryImpl

    client = ClientWrapper.get_instance()
    task_repository = TaskRepositoryImpl(notion_client_wrapper=client)
    daily_log_repository = DailyLogRepositoryImpl(client=client)

    usecase = CollectUpdatedPagesUsecase(
        is_debug=True,
        task_repository=task_repository,
        daily_log_repository=daily_log_repository,
    )
    usecase.execute(target_datetime=datetime(2024, 6, 20, 21, 0, 0, tzinfo=JST))
