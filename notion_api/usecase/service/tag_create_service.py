from lotion import Lotion
from lotion.page import PageId
from lotion.properties import Title
from typing_extensions import deprecated

from common.value.database_type import DatabaseType
from custom_logger import get_logger

logger = get_logger(__name__)


class TagCreateService:
    def __init__(self, client: Lotion | None = None) -> None:
        self.client = client or Lotion.get_instance()

    @deprecated("use add_tag_page instead")
    def add_tag(self, name: str) -> str:
        """指定されたタグをタグデータベースに追加する。タグページのIDを返却する"""
        # すでに存在するか確認
        tags = self.client.retrieve_database(database_id=DatabaseType.TAG.value, title=name)
        if len(tags) > 0:
            return tags[0].page_id.value

        # 作成
        result = self.client.create_page_in_database(
            database_id=DatabaseType.TAG.value,
            properties=[
                Title.from_plain_text(name="名前", text=name),
            ],
        )
        return result.page_id.value

    def add_tag_page(self, name: str) -> PageId:
        """指定されたタグをタグデータベースに追加する。タグページのIDを返却する"""
        tag_id = self.add_tag(name=name)
        return PageId(tag_id)
