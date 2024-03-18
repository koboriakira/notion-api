from datetime import date as DateObject
from datetime import datetime, timedelta

from custom_logger import get_logger
from domain.database_type import DatabaseType
from notion_api.notion_client_wrapper.filter.condition.date_condition import DateCondition
from notion_api.notion_client_wrapper.filter.filter_builder import FilterBuilder
from notion_client_wrapper import block
from notion_client_wrapper.base_page import BasePage
from notion_client_wrapper.block.rich_text.rich_text_builder import RichTextBuilder
from notion_client_wrapper.client_wrapper import ClientWrapper
from notion_client_wrapper.filter.condition.string_condition import StringCondition
from notion_client_wrapper.properties.last_edited_time import LastEditedTime
from notion_client_wrapper.properties.title import Title
from util.datetime import JST, jst_today

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
    def __init__(self, is_debug: bool|None = None) -> None:
        self.client = ClientWrapper.get_instance()
        self.is_debug = is_debug

    def execute(self, target_date: DateObject | None = None) -> None:
        # 初期値の整理
        target_date = target_date if target_date is not None else jst_today()

        # デイリーログを取得
        daily_log = self._find_daily_log(target_date=target_date)
        daily_log_id = daily_log.id

        for title, database_type in DATABASE_DICT.items():
            pages = self._get_latest_items(target_date=target_date, database_type=database_type)
            self._append_relation_to_daily_log(daily_log_id=daily_log_id, title=title, pages=pages)

    def _find_daily_log(self, target_date: DateObject) -> BasePage:
        """ 指定された日付のデイリーログを取得する """
        title_property = Title.from_plain_text(name=DATABASE_TYPE_DAILY_LOG.title_name(), text=target_date.isoformat())
        filter_param = FilterBuilder().add_condition(
            StringCondition.equal(property=title_property),
        ).build()

        pages = self.client.retrieve_database(
            database_id=DATABASE_TYPE_DAILY_LOG.value,
            filter_param=filter_param,
        )
        if len(pages) == 0:
            error_message = f"指定された日付のデイリーログは存在しません。デイリーログを作成してから再実行してください。: {target_date.isoformat()}"
            raise ValueError(error_message)
        return pages[0]

    def _get_latest_items(self, target_date: DateObject, database_type: DatabaseType) -> list[BasePage]:
        """ 指定されたカテゴリの、最近更新されたページIDを取得する """
        start = datetime(target_date.year, target_date.month, target_date.day, 0, 0, 0, tzinfo=JST)
        last_edited_time_start = LastEditedTime.create(
            name=database_type.name_last_edited_time(), value=start)
        end = start + timedelta(hours=24)
        last_edited_time_end = LastEditedTime.create(
            name=database_type.name_last_edited_time(),value=end)
        filter_param = FilterBuilder().add_condition(DateCondition.on_or_after(last_edited_time_start)).add_condition(DateCondition.on_or_before(last_edited_time_end)).build()
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
    usecase = CollectUpdatedPagesUsecase(is_debug=True)
    usecase.execute(target_date=datetime(2024, 3, 18, tzinfo=JST).date())
