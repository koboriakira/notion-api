
from notion_client_wrapper.properties.relation import Relation


class Author(Relation):
    NAME = "著者"

    def __init__(self, name: str, id_list: list[str]|None = None, text_list: list[str]|None = None) -> None:
        super().__init__(
            name=name,
            id_list=id_list,
            text_list=text_list,
        )

    @classmethod
    def create(cls: "Author", id_list: list[str]|None = None, text_list: list[str]|None = None) -> "Author":
        return Author(name=cls.NAME, id_list=id_list, text_list=text_list)
