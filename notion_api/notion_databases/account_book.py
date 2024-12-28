from enum import Enum

from lotion import notion_database, notion_prop
from lotion.base_page import BasePage
from lotion.properties import Checkbox, Date, MultiSelect, Number, Select, Title


class CategoryType(Enum):
    RESIDENCE_UTILITIES_COMMUNICATIONS = "住居・水道光熱・通信費"
    MISC = "雑費"
    SPECIAL_EXPENSES_TJPW = "特別費(東京女子プロレス)"
    HOBBY_SOCIAL_EXPENSES = "趣味・交際費"
    CLOTHING_BEAUTY_EXPENSES = "被服・美容費"
    FOOD_DAILY_LIVING_EXPENSES = "食費・日用品・生活費"


class AccountTag(Enum):
    MUSIC_BAR_T = "music bar t"


@notion_prop("名前")
class AccountTitle(Title):
    pass


@notion_prop("日付")
class AccountDate(Date):
    pass


@notion_prop("金額")
class Price(Number):
    pass


@notion_prop("固定費")
class IsFixedCost(Checkbox):
    pass


@notion_prop("費目")
class Category(Select):
    pass


@notion_prop("タグ")
class Tag(MultiSelect):
    pass


@notion_database("f2c5fc6e-4c27-429f-add5-2279f1f84e8d")
class AccountBook(BasePage):
    """家計簿クラス"""

    account_title: AccountTitle
    date: AccountDate
    price: Price
    is_fixed_cost: IsFixedCost
    category: Category
    tag: Tag
