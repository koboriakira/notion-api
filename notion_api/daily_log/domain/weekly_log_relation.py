from notion_client_wrapper.page.page_id import PageId
from notion_client_wrapper.properties.relation import Relation


class WeeklyLogRelation(Relation):
    NAME = "💭 ウィークリーログ"

    def __init__(self, id_list: list[PageId]) -> None:
        super().__init__(
            name=self.NAME,
            id_list=list({id_.value for id_ in id_list}),
        )

    @staticmethod
    def empty() -> "WeeklyLogRelation":
        return WeeklyLogRelation(id_list=[])

    @staticmethod
    def from_id_list(id_list: list[PageId]) -> "WeeklyLogRelation":
        return WeeklyLogRelation(id_list=id_list)

    def add(self, page_id: PageId) -> "WeeklyLogRelation":
        page_id_list = [PageId(id_) for id_ in self.id_list]
        return WeeklyLogRelation(id_list=[*page_id_list, page_id])
