from lotion.properties import Relation


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
    def from_id_list(id_list: list[str]) -> "TagRelation":
        return TagRelation(id_list=id_list)

    @staticmethod
    def from_page_id_list(id_list: list[str]) -> "TagRelation":
        return TagRelation(id_list=id_list)

    def add(self, notion_page_id: str) -> "TagRelation":
        return TagRelation(id_list=[*self.id_list, notion_page_id])
