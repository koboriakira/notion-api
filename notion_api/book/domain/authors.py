from lotion.properties import Relation


class Authors(Relation):
    NAME = "著者"

    def __init__(self, id_list: list[str]) -> None:
        super().__init__(
            name=self.NAME,
            id_list=id_list,
        )

    @staticmethod
    def empty() -> "Authors":
        return Authors(id_list=[])

    @staticmethod
    def from_id_list(id_list: list[str]) -> "Authors":
        return Authors(id_list=id_list)

    def add(self, page_id: str) -> "Authors":
        return Authors(id_list=[*self.id_list, page_id])
