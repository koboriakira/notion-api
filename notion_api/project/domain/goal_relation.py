from lotion.properties import Relation


class GoalRelation(Relation):
    NAME = "目標"

    def __init__(self, id_list: list[str] | None = None) -> None:
        super().__init__(
            name=self.NAME,
            id_list=list(set(id_list or [])),
        )

    @staticmethod
    def empty() -> "GoalRelation":
        return GoalRelation(id_list=[])

    @staticmethod
    def from_id_list(id_list: list[str]) -> "GoalRelation":
        return GoalRelation(id_list=id_list)

    def add(self, notion_page_id: str) -> "GoalRelation":
        return GoalRelation(id_list=[*self.id_list, notion_page_id])
