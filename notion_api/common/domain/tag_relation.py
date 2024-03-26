from common.value.notion_page_id import NotionPageId
from notion_client_wrapper.properties.relation import Relation


class TagRelation(Relation):
    NAME = "タグ"

    def __init__(
            self,
            id_list: list[str]|None = None) -> None:
        super().__init__(
            name=self.NAME,
            id_list=list(set(id_list or [])),
        )

    @staticmethod
    def empty() -> "TagRelation":
        return TagRelation(id_list=[])

    @staticmethod
    def from_id_list(id_list: list[str|NotionPageId]) -> "TagRelation":
        return TagRelation(
            id_list=[id_.value if isinstance(id_, NotionPageId) else id_ for id_ in id_list],
        )

    def add(self, notion_page_id: NotionPageId|str) -> "TagRelation":
        str_value = notion_page_id.value if isinstance(notion_page_id, NotionPageId) else notion_page_id
        return TagRelation(id_list=[*self.id_list, str_value])
