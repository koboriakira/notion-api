from enum import Enum

from lotion.properties import Select

kind_map = {
    "自動作成": {"selected_id": "pMjN", "selected_color": "gray"},
    "まだつくってない": {"selected_id": "426fbc68-2502-48ab-a64c-782149f10b03", "selected_color": "default"},
    "殿堂入り": {"selected_id": "5086e21b-258e-440e-802d-b9c032b2a537", "selected_color": "green"},
    "レシピ入り": {"selected_id": "1455196c-b429-46c9-bfc8-0e50424a7d2e", "selected_color": "blue"},
    "アーカイブ": {"selected_id": "KxYs", "selected_color": "red"},
}


class RecipeKindType(Enum):
    YET = "まだつくってない"
    CLASSIC = "殿堂入り"
    COOKED = "レシピ入り"
    ARCHIVE = "アーカイブ"
    AUTO = "自動作成"

    @staticmethod
    def from_text(text: str) -> "RecipeKindType":
        for kind_type in RecipeKindType:
            if kind_type.value == text:
                return kind_type
        msg = f"RecipeKindType に存在しない値です: {text}"
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


class RecipeKind(Select):
    NAME = "状態"

    def __init__(self, kind_type: RecipeKindType) -> None:
        super().__init__(
            name=self.NAME,
            selected_name=kind_type.selected_name,
            selected_id=kind_type.selected_id,
            selected_color=kind_type.selected_color,
            id=None,
        )
