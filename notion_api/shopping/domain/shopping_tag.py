from dataclasses import dataclass

from notion_client_wrapper.properties.multi_select import MultiSelect, MultiSelectElement

KIND_LIST = [
    {"name": "野菜・くだもの", "id": "9df15b00-acca-431e-9061-108048447758"},
    {"name": "薬味", "id": "c28b038e-eccb-4ed8-b43f-7ab77ebf0144"},
    {"name": "日用品", "id": "f073a502-920e-4ec9-9602-4300acd981f2"},
    {"name": "調味料", "id": "9725b89c-50bb-42b2-b92b-1296d80fde87"},
    {"name": "必須", "id": "ec5bcf82-b004-47d3-8708-922c2269425e"},
    {"name": "あらた", "id": "025bec91-b564-4bc6-a6f6-2780e2f47dbf"},
    {"name": "練り物", "id": "598a6d35-4d21-485a-ab1b-3e3a33cbae68"},
    {"name": "豆", "id": "be91882b-87a9-4b95-801f-77756e1f182d"},
    {"name": "乳製品", "id": "44448141-9cd0-48db-bb57-6f11caff0a92"},
    {"name": "飲み物", "id": "d9fd42f9-838a-4c0f-a941-14a16f4aad56"},
    {"name": "穀物類・小麦", "id": "67d36e5c-f45e-4835-8c9b-bb6324c9f5e3"},
    {"name": "長期", "id": "a3a59743-2939-40de-80ea-60a0909d0c71"},
    {"name": "肉・魚", "id": "635ae1da-30f8-4d1d-b111-6c7982fd8532"},
    {"name": "おかし", "id": "611640e2-98eb-476f-9394-b72013efdf9d"},
    {"name": "卵", "id": "8ae38d99-efb1-4362-8237-0fa33d11f7b1"},
]


@dataclass(frozen=True)
class ShoppingTagType:
    name: str
    id: str

    @staticmethod
    def from_text(text: str) -> "ShoppingTagType":
        for kind_type in KIND_LIST:
            if kind_type["name"] == text:
                return ShoppingTagType(**kind_type)
        msg = f"ShoppingTagType に存在しない値です: {text}"
        raise ValueError(msg)

    def __dict__(self) -> dict[str, str]:
        return {"name": self.name, "id": self.id}

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, ShoppingTagType):
            return False
        return self.id == __value.id


@dataclass(frozen=True)
class ShoppingTagTypes:
    values: list[ShoppingTagType]

    def __post_init__(self) -> None:
        for value in self.values:
            if not isinstance(value, ShoppingTagType):
                msg = f"[{type(self)} Invalid type for {value}: {type(value)}"
                raise TypeError(msg)

    def to_multi_select_elements(self) -> list[MultiSelectElement]:
        return [MultiSelectElement(**kind.__dict__()) for kind in self.values]


class ShoppingTag(MultiSelect):
    NAME = "タグ"

    def __init__(self, kind_types: ShoppingTagTypes) -> None:
        super().__init__(
            name=self.NAME,
            values=kind_types.to_multi_select_elements(),
        )


if __name__ == "__main__":
    # 最新の情報を取得するときに使う
    # python -m notion_api.shopping.domain.shopping_tag
    from common.value.database_type import DatabaseType
    from lotion import Lotion

    pages = Lotion.get_instance().retrieve_database(
        database_id=DatabaseType.SHOPPING.value,
    )

    result = []
    for page in pages:
        select_property = page.get_multi_select(name=ShoppingTag.NAME)
        if select_property is None:
            continue
        values = select_property.values
        result.extend([{"name": value.name, "id": value.id} for value in values])
    # uniqueにする
    result = list({value["name"]: value for value in result}.values())
    import json

    print(json.dumps(result, ensure_ascii=False))
