from dataclasses import dataclass

from lotion.properties import MultiSelect
from lotion.properties.multi_select import MultiSelectElement

KIND_LIST = [{"name": "music bar t", "id": "53bf9fc9-7e08-42d0-89fa-e67c224ba921"}]


@dataclass(frozen=True)
class TagType:
    name: str
    id: str

    @staticmethod
    def from_text(text: str) -> "TagType":
        for kind_type in KIND_LIST:
            if kind_type["name"] == text:
                return TagType(**kind_type)
        msg = f"TagType に存在しない値です: {text}"
        raise ValueError(msg)

    def __dict__(self) -> dict[str, str]:
        return {"name": self.name, "id": self.id}

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, TagType):
            return False
        return self.id == __value.id


@dataclass(frozen=True)
class TagTypes:
    values: list[TagType]

    def __post_init__(self) -> None:
        for value in self.values:
            if not isinstance(value, TagType):
                msg = f"[{type(self)} Invalid type for {value}: {type(value)}"
                raise TypeError(msg)

    def to_multi_select_elements(self) -> list[MultiSelectElement]:
        return [MultiSelectElement(**kind.__dict__()) for kind in self.values]


class Tag(MultiSelect):
    NAME = "タグ"

    def __init__(self, kind_types: TagTypes) -> None:
        super().__init__(
            name=self.NAME,
            values=kind_types.to_multi_select_elements(),
        )


if __name__ == "__main__":
    # 最新の情報を取得するときに使う
    # python -m notion_api.account_book.domain.tag
    from lotion import Lotion

    from common.value.database_type import DatabaseType

    pages = Lotion.get_instance().retrieve_database(
        database_id=DatabaseType.ACCOUNT_BOOK.value,
    )

    result = []
    for page in pages:
        select_property = page.get_multi_select(name=Tag.NAME)
        if select_property is None:
            continue
        values = select_property.values
        result.extend([{"name": value.name, "id": value.id} for value in values])
    # uniqueにする
    result = list({value["name"]: value for value in result}.values())
    import json

    print(json.dumps(result, ensure_ascii=False))
