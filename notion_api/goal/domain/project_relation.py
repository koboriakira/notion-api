from notion_client_wrapper.page.page_id import PageId
from notion_client_wrapper.properties.relation import Relation


class ProjectRelation(Relation):
    NAME = "プロジェクト"

    def __init__(self, id_list: list[PageId]) -> None:
        super().__init__(
            name=self.NAME,
            id_list=list(set([id_.value for id_ in id_list])),
        )

    @staticmethod
    def empty() -> "ProjectRelation":
        return ProjectRelation(id_list=[])

    @staticmethod
    def from_id_list(id_list: list[PageId]) -> "ProjectRelation":
        return ProjectRelation(id_list=id_list)

    def add(self, page_id: PageId) -> "ProjectRelation":
        page_id_list = [PageId(id_) for id_ in self.id_list]
        return ProjectRelation(id_list=[*page_id_list, page_id])
