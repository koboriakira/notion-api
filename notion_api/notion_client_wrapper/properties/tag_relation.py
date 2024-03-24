from notion_client_wrapper.properties.relation import Relation


class TagRelation(Relation):
    NAME = "タグ"

    def __init__(
            self,
            id_list: list[str]|None = None) -> None:
        super().__init__(
            name=self.NAME,
            id_list=id_list,
        )

    @staticmethod
    def empty() -> "TagRelation":
        return TagRelation(id_list=[])

    @staticmethod
    def from_id_list(id_list: list[str]) -> "TagRelation":
        return TagRelation(
            id_list=id_list,
        )

    def append_relation_id(self, relation_id: str) -> "TagRelation":
        return TagRelation(
            id_list=[*self.id_list, relation_id],
        )
