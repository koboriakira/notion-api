from typing import Optional
from datetime import date as Date
from domain.database_type import DatabaseType
from notion_client_wrapper.client_wrapper import ClientWrapper
from notion_client_wrapper.properties import Title, Text, Relation, Url, Date, Cover, Status
from notion_client_wrapper.block.rich_text.rich_text_builder import RichTextBuilder
from notion_client_wrapper.block import Paragraph
from usecase.service.tag_create_service import TagCreateService
from custom_logger import get_logger

logger = get_logger(__name__)

class AddWebclipUsecase:
    def __init__(self):
        self.client = ClientWrapper.get_instance()
        self.tag_create_service = TagCreateService()

    def execute(self,
                url: str,
                title: str,
               summary: str,
               tags: list[str],
               status: str,
               cover: Optional[str] = None,
               text: Optional[str] = None,
               ) -> dict:
        logger.info("execute")

        searched_webclips = self.client.retrieve_database(
            database_id=DatabaseType.WEBCLIP.value,
            title=title,
        )
        if len(searched_webclips) > 0:
            logger.info("Webclip is already registered")
            page = searched_webclips[0]
            return {
                "id": page.id,
                "url": page.url
            }
        logger.info("Create a Webclip")

        # タグを作成
        tag_page_ids:list[str] = []
        for tas in tags:
            page_id = self.tag_create_service.add_tag(name=tas)
            tag_page_ids.append(page_id)

        # 新しいページを作成
        properties=[
                Title.from_plain_text(name="名前", text=title),
                Url.from_url(name="URL", url=url),
                Status.from_status_name(name="ステータス", status_name=status),
            ]
        if len(tag_page_ids) > 0:
            properties.append(Relation.from_id_list(name="タグ", id_list=tag_page_ids))
        if summary is not None:
            properties.append(Text.from_plain_text(name="概要", text=summary))
        result = self.client.create_page_in_database(
            database_id=DatabaseType.WEBCLIP.value,
            cover=Cover.from_external_url(cover) if cover is not None else None,
            properties=properties
        )
        page = {
            "id": result["id"],
            "url": result["url"]
        }

        # ページ本文を追加
        if text is not None:
            rich_text = RichTextBuilder.get_instance().add_text(text).build()
            paragraph = Paragraph.from_rich_text(rich_text=rich_text)
            self.client.append_block(block_id=page["id"], block=paragraph)

        return page
