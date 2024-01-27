from typing import Optional
from datetime import date as Date
from domain.database_type import DatabaseType
from notion_client_wrapper.client_wrapper import ClientWrapper
from notion_client_wrapper.properties import Title, Text, Relation, Url, Date, Cover
from notion_client_wrapper.block.block_factory import BlockFactory
from usecase.service.tag_create_service import TagCreateService
from custom_logger import get_logger

logger = get_logger(__name__)

class AppendFeelingUsecase:
    def __init__(self):
        self.client = ClientWrapper.get_instance()

    def execute(self,
                page_id: str,
                value: str,
                ) -> dict:
        logger.info("AppendFeelingUsecase start")
        page = self.client.retrieve_page(page_id=page_id)
        feeling = page.get_text(name="気持ち").append_text(text=value)
        self.client.update_page(
            page_id=page_id,
            properties=[feeling]
        )
