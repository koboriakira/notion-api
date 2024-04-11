from common.value.database_type import DatabaseType
from custom_logger import get_logger
from notion_client_wrapper.client_wrapper import ClientWrapper
from notion_client_wrapper.properties import Title

logger = get_logger(__name__)


class TagCreateService:
    def __init__(self, client: ClientWrapper | None = None) -> None:
        self.client = client or ClientWrapper.get_instance()

    def add_tag(self, name: str) -> str:
        """指定されたタグをタグデータベースに追加する。タグページのIDを返却する"""
        # すでに存在するか確認
        tags = self.client.retrieve_database(database_id=DatabaseType.TAG.value, title=name)
        if len(tags) > 0:
            return tags[0].id

        # 作成
        result = self.client.create_page_in_database(
            database_id=DatabaseType.TAG.value,
            properties=[
                Title.from_plain_text(name="名前", text=name),
            ],
        )
        return result["id"]
