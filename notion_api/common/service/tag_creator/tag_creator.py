from common.domain.tag_relation import TagRelation
from domain.database_type import DatabaseType
from notion_client_wrapper.client_wrapper import ClientWrapper
from notion_client_wrapper.filter.filter_builder import FilterBuilder
from notion_client_wrapper.properties import Title


class TagCreator:
    def __init__(self, client:ClientWrapper|None=None) -> None:
        self.client = client or ClientWrapper.get_instance()

    def execute(self, name_list: list[str]|str|None) -> TagRelation:
        """指定されたタグをタグデータベースに追加する。タグページのIDを返却する。"""
        if name_list is None:
            return TagRelation.empty()
        name_list = list(set(name_list)) if isinstance(name_list, list) else [name_list]

        title_properties = [Title.from_plain_text(name="名前", text=name) for name in name_list]
        tag_page_list = [self.__create(title_property) for title_property in title_properties]
        tag_page_id_list = [tag_page["id"] for tag_page in tag_page_list]
        return TagRelation.from_id_list(id_list=tag_page_id_list)

    def __create(self, title_property: Title) -> dict:
        # すでに存在するか確認
        filter_param = FilterBuilder.build_simple_equal_condition(title_property)
        tags = self.client.retrieve_database(
            database_id=DatabaseType.TAG.value,
            filter_param=filter_param)
        if len(tags) > 0:
            return {
                "id": tags[0].id,
                # "url": tags[0].url,
            }

        # 作成
        tag_page = self.client.create_page_in_database(
            database_id=DatabaseType.TAG.value,
            properties=[title_property],
        )
        return {
            "id": tag_page["id"],
            # "url": tag_page["url"],
        }


if __name__ == "__main__":
    # python -m notion_api.common.service.tag_creator.tag_creator
    tag_creator = TagCreator()
    tag_creator.execute(["tjpw"])
