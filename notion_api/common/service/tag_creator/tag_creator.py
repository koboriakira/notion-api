from common.value.database_type import DatabaseType
from notion_client_wrapper.client_wrapper import ClientWrapper
from notion_client_wrapper.filter.filter_builder import FilterBuilder
from notion_client_wrapper.page.page_id import PageId
from notion_client_wrapper.properties import Title


class TagCreator:
    DATABASE_ID = DatabaseType.TAG.value

    def __init__(self, client: ClientWrapper | None = None) -> None:
        self.client = client or ClientWrapper.get_instance()

    def execute(self, tag: list[str] | str | None) -> list[PageId]:
        """指定されたタグをタグデータベースに追加する。タグページのIDを返却する。"""
        if tag is None:
            return []

        tag_list = list(set(tag)) if isinstance(tag, list) else [tag]
        return [self.__create(t) for t in tag_list]

    def __create(self, title: str) -> PageId:
        # すでに存在するか確認
        filter_param = FilterBuilder.build_title_equal_condition(title=title)
        tags = self.client.retrieve_database(database_id=self.DATABASE_ID, filter_param=filter_param)
        if len(tags) > 0:
            return PageId(tags[0].id)

        # 作成
        tag_page = self.client.create_page_in_database(
            database_id=self.DATABASE_ID,
            properties=[Title.from_plain_text(name="名前", text=title)],
        )
        return PageId(tag_page["id"])


if __name__ == "__main__":
    # python -m notion_api.common.service.tag_creator.tag_creator
    tag_creator = TagCreator()
    tag_creator.execute(["tjpw"])
