from lotion.page.page_id import PageId
from lotion.properties import Relation


class Authors(Relation):
    NAME = "著者"

    def __init__(self, id_list: list[PageId]) -> None:
        super().__init__(
            name=self.NAME,
            id_list=list({id_.value for id_ in id_list}),
        )

    @staticmethod
    def empty() -> "Authors":
        return Authors(id_list=[])

    @staticmethod
    def from_id_list(id_list: list[PageId]) -> "Authors":
        return Authors(id_list=id_list)

    def add(self, page_id: PageId) -> "Authors":
        page_id_list = [PageId(id_) for id_ in self.id_list]
        return Authors(id_list=[*page_id_list, page_id])
