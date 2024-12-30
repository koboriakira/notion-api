from enum import Enum


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
