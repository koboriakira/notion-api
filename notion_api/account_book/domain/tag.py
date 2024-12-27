from dataclasses import dataclass

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
