from lotion import Lotion

from notion_databases.tag import Tag, TagTitle


class TagCreator:
    def __init__(self, client: Lotion | None = None) -> None:
        self.client = client or Lotion.get_instance()

    def execute(self, tag: list[str] | str | None) -> list[str]:
        """指定されたタグをタグデータベースに追加する。タグページのIDを返却する。"""
        if tag is None:
            return []

        tag_list = list(set(tag)) if isinstance(tag, list) else [tag]
        return [self.__create(t) for t in tag_list]

    def __create(self, title: str) -> str:
        # すでに存在するか確認
        tag_title = TagTitle.from_plain_text(title, "名前")
        tags = self.client.search_pages(Tag, tag_title)
        if len(tags) > 0:
            return tags[0].id

        # 作成
        tag_page = self.client.update(Tag.create([tag_title]))
        return tag_page.id


if __name__ == "__main__":
    # python -m notion_api.common.service.tag_creator.tag_creator
    tag_creator = TagCreator()
    tag_creator.execute(["tjpw"])
