from lotion.properties import Relation


class WeeklyLogRelation(Relation):
    NAME = "💭 ウィークリーログ"

    def __init__(self, id_list: list[str]) -> None:
        super().__init__(
            name=self.NAME,
            id_list=id_list,
        )

    @staticmethod
    def empty() -> "WeeklyLogRelation":
        return WeeklyLogRelation(id_list=[])

    @staticmethod
    def from_id_list(id_list: list[str]) -> "WeeklyLogRelation":
        return WeeklyLogRelation(id_list=id_list)

    def add(self, page_id: str) -> "WeeklyLogRelation":
        return WeeklyLogRelation(id_list=[*self.id_list, page_id])
