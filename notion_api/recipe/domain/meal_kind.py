from dataclasses import dataclass
from enum import Enum


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


@dataclass(frozen=True)
class MealKindTypes:
    values: list[MealKindType]

    def __post_init__(self) -> None:
        for value in self.values:
            if not isinstance(value, MealKindType):
                msg = f"[{type(self)} Invalid type for {value}: {type(value)}"
                raise TypeError(msg)
