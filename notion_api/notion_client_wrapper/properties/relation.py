from dataclasses import dataclass

from notion_client_wrapper.properties.property import Property


@dataclass
class Relation(Property):
    id_list: list[str]
    text_list: list[str] # NOTE: Notionのデータとしては扱わない。id_listに変換するために必要になることが多いため
    type: str = "relation"
    has_more: bool = False

    def __init__(
            self,
            name: str,
            id: str | None = None,
            id_list: list[str]|None = None,
            text_list: list[str]|None = None,
            has_more: bool|None = None):
        self.name = name
        self.id = id
        self.id_list = id_list or []
        self.text_list = text_list or []
        self.has_more = bool(has_more)

    def is_unconverted_id_list(self) -> bool:
        """text_listがあるがid_listがない場合にTrueを返す"""
        return len(self.text_list) > 0 and len(self.id_list) == 0


    @staticmethod
    def of(name: str, property: dict[str, str]) -> "Relation":
        id_list = list(map(lambda r: r["id"], property["relation"]))
        return Relation(
            name=name,
            id_list=id_list,
            has_more=property["has_more"])

    @staticmethod
    def from_id_list(name: str, id_list: list[str]) -> "Relation":
        return Relation(
            name=name,
            id_list=id_list,
        )

    @classmethod
    def from_id(cls, name: str, id: str) -> "Relation":
        return cls.from_id_list(name=name, id_list=[id])

    def __dict__(self):
        result = {
            "type": self.type,
            "relation": [
                {
                    "id": id,
                } for id in self.id_list
            ],
            "has_more": self.has_more,
        }
        if self.id is not None:
            result["relation"]["id"] = self.id
        return {
            self.name: result,
        }

    def value_for_filter(self) -> str:
        raise NotImplementedError
