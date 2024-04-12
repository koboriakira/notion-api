from dataclasses import dataclass
from enum import Enum

from notion_client_wrapper.properties.multi_select import MultiSelect, MultiSelectElement

KIND_LIST = [
    {"name": "副菜", "id": "f1557d37-1470-4d8a-8010-0cbfcac8481a"},
    {"name": "主菜", "id": "cf981363-bf42-4503-b693-934a6568522f"},
    {"name": "ごはん", "id": "e2c07af0-1fbe-41fa-b79c-0957052f61b8"},
    {"name": "デザート", "id": "0dcc4be0-4371-4a7b-982b-8383de16089f"},
    {"name": "あらたも食べれる", "id": "429a4112-f2fe-4a00-a2fc-99ecdd512518"},
    {"name": "ヘルシー", "id": "1b77fcd4-8055-4609-9d8a-afbabddaa941"},
    {"name": "おつまみ", "id": "86e96eab-57c7-4feb-a127-8cfce21cabdd"},
    {"name": "その他", "id": "0d78d4a1-1f0d-4ae6-8d11-07dbe86922c8"},
    {"name": "麺類", "id": "315b26cf-3aa5-43f8-85d9-edee2e9c9e1e"},
    {"name": "パン", "id": "a37cefcc-c552-43e0-9dd9-ea2f4056ade2"},
    {"name": "丼もの", "id": "88128e13-7a54-4ab2-a7a3-9b1da3a1a207"},
    {"name": "野菜", "id": "f360070a-5bc3-49e8-9c3d-989a85ab1f1f"},
    {"name": "飲み物", "id": "7a102664-67cb-42db-b4ec-fc68fcdc5a2a"},
    {"name": "朝食", "id": "440d21d3-1145-4fd9-9a3e-d2d82f96f7cc"},
]


def find_kind(name: str) -> dict[str, str]:
    for kind in KIND_LIST:
        if kind["name"] == name:
            return kind
    raise ValueError(f"存在しない種類です: {name}")


class MealKindType(Enum):
    SIDE_DISH = "副菜"
    MAIN_DISH = "主菜"
    RICE = "ごはん"
    DESSERT = "デザート"
    ARATA = "あらたも食べれる"
    HEALTHY = "ヘルシー"
    SNACK = "おつまみ"
    OTHER = "その他"
    NOODLE = "麺類"
    BREAD = "パン"
    BOWL = "丼もの"
    VEGETABLE = "野菜"
    DRINK = "飲み物"
    BREAKFAST = "朝食"

    @staticmethod
    def from_text(text: str) -> "MealKindType":
        for kind_type in MealKindType:
            if kind_type.value == text:
                return kind_type
        msg = f"MealKindType に存在しない値です: {text}"
        raise ValueError(msg)

    def __dict__(self) -> dict[str, str]:
        return find_kind(name=self.value)


@dataclass(frozen=True)
class MealKindTypes:
    values: list[MealKindType]

    def __post_init__(self) -> None:
        for value in self.values:
            if not isinstance(value, MealKindType):
                msg = f"[{type(self)} Invalid type for {value}: {type(value)}"
                raise TypeError(msg)

    def to_multi_select_elements(self) -> list[MultiSelectElement]:
        return [MultiSelectElement(**kind.__dict__()) for kind in self.values]


class MealKind(MultiSelect):
    NAME = "種類"

    def __init__(self, kind_types: MealKindTypes) -> None:
        super().__init__(
            name=self.NAME,
            values=kind_types.to_multi_select_elements(),
        )
