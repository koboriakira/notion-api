from enum import Enum


class RecipeKindType(Enum):
    YET = "まだつくってない"
    CLASSIC = "殿堂入り"
    COOKED = "レシピ入り"
    ARCHIVE = "アーカイブ"
    AUTO = "自動作成"
