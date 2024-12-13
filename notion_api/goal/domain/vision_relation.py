from notion_client_wrapper.page.page_id import PageId
from lotion.properties import Relation


class VisionRelation(Relation):
    NAME = "ミッション・ビジョン"

    def __init__(self, id_list: list[PageId]) -> None:
        super().__init__(
            name=self.NAME,
            id_list=list(set([id_.value for id_ in id_list])),
        )

    @staticmethod
    def empty() -> "VisionRelation":
        return VisionRelation(id_list=[])

    @staticmethod
    def from_id_list(id_list: list[PageId]) -> "VisionRelation":
        return VisionRelation(id_list=id_list)

    def add(self, page_id: PageId) -> "VisionRelation":
        page_id_list = [PageId(id_) for id_ in self.id_list]
        return VisionRelation(id_list=[*page_id_list, page_id])
