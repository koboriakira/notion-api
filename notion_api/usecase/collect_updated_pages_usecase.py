import os
from datetime import date as DateObject
from notion_client_wrapper.base_page import BasePage
from notion_client_wrapper.client_wrapper import ClientWrapper
from notion_client_wrapper import block
from domain.database_type import DatabaseType
from notion_client_wrapper.block.rich_text.rich_text_builder import RichTextBuilder

DATABASE_DICT = {
    "今日更新したタスク": DatabaseType.TASK,
    "今日更新したプロジェクト": DatabaseType.PROJECT,
    "今日更新したZettlekasten": DatabaseType.ZETTLEKASTEN,
    "今日読んだ・登録した書籍": DatabaseType.BOOK,
    "今日更新したwebclip": DatabaseType.WEBCLIP,
    "今日観たプロレス": DatabaseType.PROWRESTLING,
    "今日更新・登録したレシピ": DatabaseType.RECIPE,
    "今日観た動画": DatabaseType.VIDEO,
    "今日聴いた音楽": DatabaseType.MUSIC,
}

def filter_in_day(date: DateObject, page: BasePage) -> bool:
    """ 指定された日付に作成もしくは更新されたページかどうかを判定する """
    return page.created_time.date == date or page.last_edited_time.date == date

def filter_in_day_with_only_created(date: DateObject, page: BasePage) -> bool:
    """ 指定された日付に作成されたページかどうかを判定する"""
    return page.created_time.date == date

class CollectUpdatedPagesUsecase:
    def __init__(self):
        self.client = ClientWrapper(notion_secret=os.getenv("NOTION_SECRET"))

    def execute(self, date: DateObject = DateObject.today()):
        daily_log = self.client.retrieve_database(
            database_id=DatabaseType.DAILY_LOG.value,
            title=date.isoformat()
        )
        daily_log_id = daily_log[0].id

        for title, database_type in DATABASE_DICT.items():
            pages = self._get_latest_items(date=date, database_type=database_type)
            self._append_relation_to_daily_log(daily_log_id=daily_log_id, title=title, pages=pages)


    def _get_latest_items(self, date: DateObject, database_type: DatabaseType, only_created: bool = False) -> list[BasePage]:
        """ 指定されたカテゴリの、最近更新されたページIDを取得する """
        pages = self.client.retrieve_database(
            database_id=database_type.value
        )
        filter_func = filter_in_day_with_only_created if only_created else filter_in_day
        pages = list(filter(lambda page: filter_func(date=date, page=page), pages))
        return pages

    def _append_relation_to_daily_log(self, daily_log_id: str, title: str, pages: list[BasePage]) -> None:
        if len(pages) == 0:
            return
        # 見出しタグをつける
        heading = block.Heading.from_plain_text(heading_size=2, text=title)
        self.client.append_block(block_id=daily_log_id,block=heading)

        # バックリンクを記録する
        for page in pages:
            rich_text = RichTextBuilder.get_instance().add_page_mention(page_id=page.id).build()
            paragraph = block.Paragraph.from_rich_text(rich_text=rich_text)
            self.client.append_block(
                block_id=daily_log_id,
                block=paragraph
            )

if __name__ == "__main__":
    # python -m usecase.collect_updated_pages_usecase
    usecase = CollectUpdatedPagesUsecase()
    usecase.execute()
