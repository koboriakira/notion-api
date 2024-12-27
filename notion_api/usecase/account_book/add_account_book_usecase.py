from datetime import date

from lotion import Lotion
from lotion.properties import Properties

from account_book.domain.account_book import AccountBook, AccountDate, AccountTitle, Category, IsFixedCost, Price, Tag


class AddAccountBookUsecase:
    def __init__(
        self,
        lotion: Lotion | None = None,
    ) -> None:
        self._lotion = lotion or Lotion.get_instance()

    def execute(  # noqa: PLR0913
        self,
        title: str,
        price: int,
        is_fixed_cost: bool | None = None,
        category: str | None = None,
        tag: list[str] | None = None,
        date_: date | None = None,
    ) -> AccountBook:
        account_book = AccountBook(properties=Properties([]))

        account_book.set_prop(AccountTitle.from_plain_text(text=title))
        account_book.set_prop(Price.from_num(value=price))

        if is_fixed_cost:
            account_book.set_prop(IsFixedCost.true())

        if category:
            _category = self._lotion.fetch_select(AccountBook, Category, category)
            account_book.set_prop(_category)

        if tag and len(tag) > 0:
            _tag = self._lotion.fetch_multi_select(AccountBook, Tag, tag)
            account_book.set_prop(_tag)

        if date_:
            account_book.set_prop(AccountDate.from_start_date(start_date=date_))

        return self._lotion.update(account_book)
