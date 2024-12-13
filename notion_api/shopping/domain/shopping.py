from dataclasses import dataclass
from datetime import date, timedelta

from lotion.base_page import BasePage
from shopping.domain.buy_status import BuyStatus, BuyStatusType
from shopping.domain.last_purchase_date import LastPurchaseDate
from shopping.domain.purchase_interval import PurchaseInterval
from shopping.domain.shopping_tag import ShoppingTagType, ShoppingTagTypes
from shopping.domain.to_buy_flag import ToBuyFlag
from util.datetime import convert_to_date_or_datetime, jst_today


@dataclass
class Shopping(BasePage):
    def reset_buy_status_type(self) -> "Shopping":
        self.properties = self.properties.append_property(BuyStatus.undone())
        self.properties = self.properties.append_property(ToBuyFlag.false())
        yesterday = jst_today() - timedelta(days=1)
        self.properties = self.properties.append_property(LastPurchaseDate.create(yesterday))
        return self

    @property
    def name(self) -> str:
        return self.get_title_text()

    @property
    def buy_status(self) -> BuyStatusType:
        status_name = self.get_status(name=BuyStatus.NAME).status_name
        return BuyStatusType.from_text(status_name)

    @property
    def purchase_interval(self) -> int:
        purchase_interval = self.get_number(name=PurchaseInterval.NAME)
        if purchase_interval is None:
            return 0
        return purchase_interval.number or 0

    @property
    def tag(self) -> ShoppingTagTypes:
        values = self.get_multi_select(name="タグ").values
        if not values or len(values) == 0:
            return ShoppingTagTypes(values=[])
        tag_list = [ShoppingTagType.from_text(text=value.name) for value in values]
        return ShoppingTagTypes(values=tag_list)

    @property
    def to_buy_flag(self) -> bool:
        return self.get_checkbox(name=ToBuyFlag.NAME).checked

    @property
    def last_purchase_date(self) -> date | None:
        last_purchase_date = self.get_date(name=LastPurchaseDate.NAME)
        if last_purchase_date is None:
            return None
        return convert_to_date_or_datetime(last_purchase_date.start)
