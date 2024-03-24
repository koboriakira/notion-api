from common.domain.value.notion_page_id import NotionPageId
from domain.database_type import DatabaseType
from notion_client_wrapper.client_wrapper import ClientWrapper
from notion_client_wrapper.filter.filter_builder import FilterBuilder
from notion_client_wrapper.properties import Title


class TagCreator:
    def __init__(self, client:ClientWrapper|None=None) -> None:
        self.client = client or ClientWrapper.get_instance()

    def execute(self, name: str) -> NotionPageId:
        """指定されたタグをタグデータベースに追加する。タグページのIDを返却する。"""
        # すでに存在するか確認
        title_property = Title.from_plain_text(name="名前", text=name)
        filter_param = FilterBuilder.build_simple_equal_condition(title_property)
        tags = self.client.retrieve_database(
            database_id=DatabaseType.TAG.value,
            filter_param=filter_param)
        if len(tags) > 0:
            return tags[0].id

        # 作成
        result = self.client.create_page_in_database(
            database_id=DatabaseType.TAG.value,
            properties=[title_property],
        )
        return NotionPageId(result["id"])
