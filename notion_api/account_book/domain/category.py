from enum import Enum


class CategoryType(Enum):
    RESIDENCE_UTILITIES_COMMUNICATIONS = "住居・水道光熱・通信費"
    MISC = "雑費"
    SPECIAL_EXPENSES_TJPW = "特別費(東京女子プロレス)"
    HOBBY_SOCIAL_EXPENSES = "趣味・交際費"
    CLOTHING_BEAUTY_EXPENSES = "被服・美容費"
    FOOD_DAILY_LIVING_EXPENSES = "食費・日用品・生活費"

    @staticmethod
    def from_text(text: str) -> "CategoryType":
        for kind_type in CategoryType:
            if kind_type.value == text:
                return kind_type
        msg = f"CategoryType に存在しない値です: {text}"
        raise ValueError(msg)
