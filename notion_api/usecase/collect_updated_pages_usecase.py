from datetime import date as DateObject
from datetime import datetime, timedelta

from custom_logger import get_logger
from domain.database_type import DatabaseType
from notion_client_wrapper import block
from notion_client_wrapper.base_page import BasePage
from notion_client_wrapper.block.rich_text.rich_text_builder import RichTextBuilder
from notion_client_wrapper.client_wrapper import ClientWrapper
from util.datetime import JST, jst_today

logger = get_logger(__name__)

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

def filter_in_day(target_date: DateObject, page: BasePage) -> bool:
    """ 指定された日付に作成もしくは更新されたページかどうかを判定する """
    end = datetime(target_date.year, target_date.month, target_date.day, 22, 0, 0, tzinfo=JST)
    start = end - timedelta(hours=24)
    return page.created_time.is_between(start=start, end=end) or page.last_edited_time.is_between(start=start, end=end)

def filter_in_day_with_only_created(target_date: DateObject, page: BasePage) -> bool:
    """ 指定された日付に作成されたページかどうかを判定する"""
    start = datetime(target_date.year, target_date.month, target_date.day, 22, 0, 0, tzinfo=JST)
    end = start + timedelta(hours=24)
    return page.created_time.is_between(start=start, end=end)

class CollectUpdatedPagesUsecase:
    def __init__(self, is_debug: bool = False):
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
        daily_log = self.client.find_page(
            database_id=DatabaseType.DAILY_LOG.value,
            title=target_date.isoformat(),
        )
        if daily_log is None:
            raise Exception("指定された日付のデイリーログは存在しません")
        return daily_log

    def _get_latest_items(self, target_date: DateObject, database_type: DatabaseType, only_created: bool|None = None) -> list[BasePage]:
        """ 指定されたカテゴリの、最近更新されたページIDを取得する """
        pages = self.client.retrieve_database(database_id=database_type.value)
        filter_func = filter_in_day_with_only_created if only_created else filter_in_day
        pages = list(filter(lambda page: filter_func(date=target_date, page=page), pages))
        return pages

    def _append_relation_to_daily_log(self, daily_log_id: str, title: str, pages: list[BasePage]) -> None:
        if len(pages) == 0:
            return
        # 見出しタグをつける
        heading = block.Heading.from_plain_text(heading_size=2, text=title)
        if not self.is_debug:
            self.client.append_block(block_id=daily_log_id,block=heading)

        # バックリンクを記録する
        for page in pages:
            rich_text = RichTextBuilder.get_instance().add_page_mention(page_id=page.id).build()
            paragraph = block.Paragraph.from_rich_text(rich_text=rich_text)
            if not self.is_debug:
                self.client.append_block(
                    block_id=daily_log_id,
                    block=paragraph,
                )
            logger.info(f"ページを追加しました: {page.get_title().text}")

if __name__ == "__main__":
    # python -m notion_api.usecase.collect_updated_pages_usecase
    usecase = CollectUpdatedPagesUsecase(is_debug=True)
    usecase.execute(date=datetime(2024, 3, 18, tzinfo=JST).date())
