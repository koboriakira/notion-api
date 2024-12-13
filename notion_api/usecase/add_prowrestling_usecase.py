from datetime import date as DateObject

from lotion import Lotion
from lotion.base_page import BasePage
from lotion.block import Paragraph
from lotion.block.rich_text import RichTextBuilder
from lotion.properties import Cover, Date, Relation, Select, Title, Url

from common.value.database_type import DatabaseType
from custom_logger import get_logger
from usecase.service.tag_create_service import TagCreateService

logger = get_logger(__name__)


def find_promotion(pages: list[BasePage], promotion_name: str) -> Select | None:
    for page in pages:
        status = page.get_select(name="団体")
        if status.selected_name == promotion_name:
            return status
    return None


class AddProwrestlingUsecase:
    def __init__(self):
        self.client = Lotion.get_instance()
        self.tag_create_service = TagCreateService()

    def execute(
        self,
        url: str,
        title: str,
        date: DateObject,
        promotion: str,
        text: str,
        tags: list[str],
        cover: str | None = None,
    ) -> dict:
        logger.info("execute")

        searched_pw_events = self.client.retrieve_database(
            database_id=DatabaseType.PROWRESTLING.value,
            title=title,
        )
        if len(searched_pw_events) > 0:
            logger.info("Event is already registered")
            page = searched_pw_events[0]
            return {
                "id": page.id,
                "url": page.url,
            }
        logger.info("Create a Event")

        # 団体の選択肢を特定
        pw_events = self.client.retrieve_database(database_id=DatabaseType.PROWRESTLING.value)
        promotion_select = find_promotion(pages=pw_events, promotion_name=promotion)

        # タグを作成
        tag_page_ids: list[str] = []
        for tas in tags:
            page_id = self.tag_create_service.add_tag(name=tas)
            tag_page_ids.append(page_id)

        # 新しいページを作成
        properties = [
            Title.from_plain_text(name="名前", text=title),
            Url.from_url(name="URL", url=url),
            Date.from_start_date(name="日付", start_date=date),
            promotion_select,
        ]
        if len(tag_page_ids) > 0:
            properties.append(Relation.from_id_list(name="タグ", id_list=tag_page_ids))
        result = self.client.create_page_in_database(
            database_id=DatabaseType.PROWRESTLING.value,
            cover=Cover.from_external_url(cover) if cover is not None else None,
            properties=properties,
        )
        page = {
            "id": result["id"],
            "url": result["url"],
        }

        # ページ本文を追加
        if text is not None or text != "":
            # textが1500文字を超える場合は、1500文字ずつ分割して追加する
            if len(text) > 1500:
                for i in range(0, len(text), 1500):
                    rich_text = RichTextBuilder.get_instance().add_text(text[i : i + 1500]).build()
                    paragraph = Paragraph.from_rich_text(rich_text=rich_text)
                    self.client.append_block(block_id=page["id"], block=paragraph)
            else:
                rich_text = RichTextBuilder.get_instance().add_text(text).build()
                paragraph = Paragraph.from_rich_text(rich_text=rich_text)
                self.client.append_block(block_id=page["id"], block=paragraph)
        return page
