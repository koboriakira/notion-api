from common.domain.tag_relation import TagRelation
from domain.database_type import DatabaseType
from notion_client_wrapper.client_wrapper import ClientWrapper
from notion_client_wrapper.filter.filter_builder import FilterBuilder
from notion_client_wrapper.properties import Title


class TagCreator:
    def __init__(self, client:ClientWrapper|None=None) -> None:
        self.client = client or ClientWrapper.get_instance()

    def execute(self, name_list: list[str]|str) -> TagRelation:
        """指定されたタグをタグデータベースに追加する。タグページのIDを返却する。"""
        name_list = name_list if isinstance(name_list, list) else [name_list]

        result = TagRelation.empty()
        for name in name_list:
            # すでに存在するか確認
            title_property = Title.from_plain_text(name="名前", text=name)
            filter_param = FilterBuilder.build_simple_equal_condition(title_property)
            tags = self.client.retrieve_database(
                database_id=DatabaseType.TAG.value,
                filter_param=filter_param)
            if len(tags) > 0:
                result = result.add(tags[0].id)

            # 作成
            tag_page = self.client.create_page_in_database(
                database_id=DatabaseType.TAG.value,
                properties=[title_property],
            )
            result = result.add(tag_page["id"])
        return result

if __name__ == "__main__":
    # python -m notion_api.common.service.tag_creator.tag_creator
    tag_creator = TagCreator()
    tag_creator.execute(["tjpw"])
