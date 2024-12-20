from lotion.properties import Relation


class ProjectRelation(Relation):
    NAME = "プロジェクト"

    def __init__(self, id_list: list[str]) -> None:
        super().__init__(
            name=self.NAME,
            id_list=id_list,
        )

    @staticmethod
    def empty() -> "ProjectRelation":
        return ProjectRelation(id_list=[])

    @staticmethod
    def from_id_list(id_list: list[str]) -> "ProjectRelation":
        return ProjectRelation(id_list=id_list)

    def add(self, page_id: str) -> "ProjectRelation":
        return ProjectRelation(id_list=[*self.id_list, page_id])
