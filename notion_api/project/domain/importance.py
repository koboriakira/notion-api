from enum import Enum


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
