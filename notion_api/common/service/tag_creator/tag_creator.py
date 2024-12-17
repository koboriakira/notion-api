from lotion import Lotion
from lotion.filter import Builder
from lotion.filter.condition import Cond, Prop
from lotion.page.page_id import PageId
from lotion.properties import Title

from common.value.database_type import DatabaseType


class TagCreator:
    DATABASE_ID = DatabaseType.TAG.value

    def __init__(self, client: Lotion | None = None) -> None:
        self.client = client or Lotion.get_instance()

    def execute(self, tag: list[str] | str | None) -> list[PageId]:
        """指定されたタグをタグデータベースに追加する。タグページのIDを返却する。"""
        if tag is None:
            return []

        tag_list = list(set(tag)) if isinstance(tag, list) else [tag]
        return [self.__create(t) for t in tag_list]

    def __create(self, title: str) -> PageId:
        # すでに存在するか確認
        builder = Builder.create().add(Prop.RICH_TEXT, "名前", Cond.EQUALS, title)
        tags = self.client.retrieve_database(database_id=self.DATABASE_ID, filter_param=builder.build())
        if len(tags) > 0:
            return tags[0].page_id

        # 作成
        tag_page = self.client.create_page_in_database(
            database_id=self.DATABASE_ID,
            properties=[Title.from_plain_text(name="名前", text=title)],
        )
        return tag_page.page_id


if __name__ == "__main__":
    # python -m notion_api.common.service.tag_creator.tag_creator
    tag_creator = TagCreator()
    tag_creator.execute(["tjpw"])
