from lotion.page import PageId
from lotion.properties import Relation


class PreviousRelation(Relation):
    NAME = "前日"

    def __init__(self, id_list: list[PageId]) -> None:
        super().__init__(
            name=self.NAME,
            id_list=list({id_.value for id_ in id_list}),
        )

    @staticmethod
    def empty() -> "PreviousRelation":
        return PreviousRelation(id_list=[])

    @staticmethod
    def from_id_list(id_list: list[PageId]) -> "PreviousRelation":
        return PreviousRelation(id_list=id_list)

    def add(self, page_id: PageId) -> "PreviousRelation":
        page_id_list = [PageId(id_) for id_ in self.id_list]
        return PreviousRelation(id_list=[*page_id_list, page_id])
