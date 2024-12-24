from lotion.properties import Relation


class PreviousRelation(Relation):
    NAME = "前日"

    def __init__(self, id_list: list[str]) -> None:
        super().__init__(
            name=self.NAME,
            id_list=id_list,
        )

    @staticmethod
    def empty() -> "PreviousRelation":
        return PreviousRelation(id_list=[])

    @staticmethod
    def from_id_list(id_list: list[str]) -> "PreviousRelation":
        return PreviousRelation(id_list=id_list)

    def add(self, page_id: str) -> "PreviousRelation":
        return PreviousRelation(id_list=[*self.id_list, page_id])
