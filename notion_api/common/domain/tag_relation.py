from lotion.page.page_id import PageId
from lotion.properties import Relation

from common.value.notion_page_id import NotionPageId


def convert_page_id(id_: str | NotionPageId | PageId) -> str:
    if isinstance(id_, PageId):
        return id_.value
    return id_.value if isinstance(id_, NotionPageId) else id_


class TagRelation(Relation):
    NAME = "タグ"

    def __init__(self, id_list: list[str] | None = None) -> None:
        super().__init__(
            name=self.NAME,
            id_list=list(set(id_list or [])),
        )

    @staticmethod
    def empty() -> "TagRelation":
        return TagRelation(id_list=[])

    @staticmethod
    def from_id_list(id_list: list[str | NotionPageId]) -> "TagRelation":
        return TagRelation(id_list=[convert_page_id(id_) for id_ in id_list])

    @staticmethod
    def from_page_id_list(id_list: list[PageId]) -> "TagRelation":
        return TagRelation(id_list=[id_.value for id_ in id_list])

    def add(self, notion_page_id: NotionPageId | str) -> "TagRelation":
        str_value = notion_page_id.value if isinstance(notion_page_id, NotionPageId) else notion_page_id
        return TagRelation(id_list=[*self.id_list, str_value])
