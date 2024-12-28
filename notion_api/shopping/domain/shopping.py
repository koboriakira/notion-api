from datetime import timedelta

from lotion import notion_database, notion_prop
from lotion.base_page import BasePage
from lotion.properties import Checkbox, Date, MultiSelect, Number, Status, Title

from common.value.database_type import DatabaseType
from shopping.domain.buy_status import BuyStatusType
from util.datetime import jst_today


@notion_prop("名前")
class ItemName(Title):
    pass


@notion_prop("購入済")
class BuyStatus(Status):
    @staticmethod
    def from_status_type(status_type: BuyStatusType) -> "BuyStatus":
        return BuyStatus.from_status_name(status_type.name)


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
