from enum import Enum

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
