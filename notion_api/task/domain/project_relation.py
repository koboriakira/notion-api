from common.value.notion_page_id import NotionPageId
from notion_client_wrapper.properties.relation import Relation


class ProjectRelation(Relation):
    NAME = "プロジェクト"

    def __init__(self, id_list: list[str] | None = None) -> None:
        super().__init__(
            name=self.NAME,
            id_list=list(set(id_list or [])),
        )

    @staticmethod
    def empty() -> "ProjectRelation":
        return ProjectRelation(id_list=[])

    @staticmethod
    def from_id_list(id_list: list[str | NotionPageId]) -> "ProjectRelation":
        return ProjectRelation(
            id_list=[id_.value if isinstance(id_, NotionPageId) else id_ for id_ in id_list],
        )

    @staticmethod
    def from_id(id_: str) -> "ProjectRelation":
        return ProjectRelation(id_list=[id_])

    def add(self, notion_page_id: NotionPageId | str) -> "ProjectRelation":
        str_value = notion_page_id.value if isinstance(notion_page_id, NotionPageId) else notion_page_id
        return ProjectRelation(id_list=[*self.id_list, str_value])
