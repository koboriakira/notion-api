from enum import Enum

from lotion.properties import Select

kind_map = {
    "⭐⭐⭐": {"selected_id": "0056a2e0-33d1-4fe5-a43e-28a703979b9d", "selected_color": "pink"},
    "⭐⭐": {"selected_id": "902b1968-ba89-4a5f-83ac-d3655c0daf10", "selected_color": "blue"},
    "⭐": {"selected_id": "8ba62578-b8c1-4c6f-a10f-5b3572fc3a12", "selected_color": "default"},
}


class ImportanceType(Enum):
    THREE = "⭐⭐⭐"
    TWO = "⭐⭐"
    ONE = "⭐"

    @staticmethod
    def from_text(text: str) -> "ImportanceType":
        for kind_type in ImportanceType:
            if kind_type.value == text:
                return kind_type
        msg = f"ImportanceType に存在しない値です: {text}"
        raise ValueError(msg)

    @property
    def selected_name(self) -> str:
        return self.value

    @property
    def selected_id(self) -> str:
        return kind_map[self.value]["selected_id"]

    @property
    def selected_color(self) -> str:
        return kind_map[self.value]["selected_color"]


class Importance(Select):
    NAME = "重要度"

    def __init__(self, kind_type: ImportanceType) -> None:
        super().__init__(
            name=self.NAME,
            selected_name=kind_type.selected_name,
            selected_id=kind_type.selected_id,
            selected_color=kind_type.selected_color,
            id=None,
        )

    @classmethod
    def create(cls: "Importance", kind_type: ImportanceType) -> "Importance":
        return cls(kind_type=kind_type)

    @classmethod
    def three(cls: "Importance") -> "Importance":
        return cls.create(kind_type=ImportanceType.THREE)

    @classmethod
    def two(cls: "Importance") -> "Importance":
        return cls.create(kind_type=ImportanceType.TWO)

    @classmethod
    def one(cls: "Importance") -> "Importance":
        return cls.create(kind_type=ImportanceType.ONE)
