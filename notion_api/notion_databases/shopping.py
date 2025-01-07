from datetime import timedelta
from enum import Enum

from lotion import notion_database, notion_prop
from lotion.base_page import BasePage
from lotion.properties import Checkbox, Date, MultiSelect, Number, Status, Title

from common.value.database_type import DatabaseType
from util.datetime import jst_today


class BuyStatusType(Enum):
    """タスクのステータス"""

    UNDONE = "未購入"
    DONE = "購入済"


class TagType(Enum):
    VEGETABLES_FRUITS = "野菜・くだもの"
    CONDIMENT = "薬味"
    DAILY_NECESSITIES = "日用品"
    SEASONING = "調味料"
    ESSENTIAL = "必須"
    NEW = "あらた"
    PASTE = "練り物"
    BEANS = "豆"
    DAIRY_PRODUCTS = "乳製品"
    DRINKS = "飲み物"
    GRAINS_WHEAT = "穀物類・小麦"
    LONG_TERM = "長期"
    MEAT_FISH = "肉・魚"
    SWEETS = "おかし"
    EGGS = "卵"


@notion_prop("名前")
class ItemName(Title):
    pass


@notion_prop("購入済")
class BuyStatus(Status):
    @staticmethod
    def from_status_type(status_type: BuyStatusType) -> "BuyStatus":
        return BuyStatus.from_status_name(status_type.value)


@notion_prop("最終購入日")
class LastPurchaseDate(Date):
    pass


@notion_prop("購入間隔")
class PurchaseInterval(Number):
    pass


@notion_prop("タグ")
class ShoppingTag(MultiSelect):
    pass


@notion_prop("買う")
class ToBuyFlag(Checkbox):
    pass


@notion_database(DatabaseType.SHOPPING.value)
class Shopping(BasePage):
    name: ItemName
    status: BuyStatus
    last_purchase_date: LastPurchaseDate
    purchase_interval: PurchaseInterval
    tags: ShoppingTag
    to_buy: ToBuyFlag

    def is_bought(self) -> bool:
        return self._get_buy_status() == BuyStatusType.DONE

    def _get_buy_status(self) -> BuyStatusType:
        return BuyStatusType(self.status.status_name)

    def reset_buy_status_type(self) -> "Shopping":
        self.properties = self.properties.append_property(BuyStatus.from_status_type(BuyStatusType.UNDONE))
        self.properties = self.properties.append_property(ToBuyFlag.false())
        yesterday = jst_today() - timedelta(days=1)
        self.properties = self.properties.append_property(LastPurchaseDate.from_start_date(yesterday))
        return self
