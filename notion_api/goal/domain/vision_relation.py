from lotion.properties import Relation


class VisionRelation(Relation):
    NAME = "ミッション・ビジョン"

    def __init__(self, id_list: list[str]) -> None:
        super().__init__(
            name=self.NAME,
            id_list=id_list,
        )

    @staticmethod
    def empty() -> "VisionRelation":
        return VisionRelation(id_list=[])

    @staticmethod
    def from_id_list(id_list: list[str]) -> "VisionRelation":
        return VisionRelation(id_list=id_list)

    def add(self, page_id: str) -> "VisionRelation":
        return VisionRelation(id_list=[*self.id_list, page_id])
