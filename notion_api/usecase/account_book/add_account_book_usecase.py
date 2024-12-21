from datetime import date

from lotion.properties import Checkbox, Date, Number, Properties, Title

from account_book.domain.account_book import AccountBook
from account_book.domain.category import Category, CategoryType
from account_book.domain.repository import AccountRepository
from account_book.domain.tag import Tag, TagType, TagTypes


class AddAccountBookUsecase:
    def __init__(
        self,
        account_book_repository: AccountRepository,
    ) -> None:
        self._account_book_repository = account_book_repository

    def execute(
        self,
        title: str,
        price: int,
        is_fixed_cost: bool | None = None,
        category: str | None = None,
        tag: list[str] | None = None,
        date_: date | None = None,
    ) -> dict[str, str]:
        account_book = self._create_entity(
            title=title,
            price=price,
            is_fixed_cost=is_fixed_cost,
            category=category,
            tag=tag,
            date_=date_,
        )
        return self._account_book_repository.save(account_book).get_id_and_url()

    def _create_entity(
        self,
        title: str,
        price: int,
        is_fixed_cost: bool | None = None,
        category: str | None = None,
        tag: list[str] | None = None,
        date_: date | None = None,
    ) -> AccountBook:
        properties = []

        _title = Title.from_plain_text(text=title)
        properties.append(_title)
        _price = Number.from_num(name="金額", value=price)
        properties.append(_price)

        if is_fixed_cost:
            _is_fixed_cost = Checkbox.true(name="固定費")
            properties.append(_is_fixed_cost)

        if category:
            _category = Category(kind_type=CategoryType.from_text(category))
            properties.append(_category)

        if tag and len(tag) > 0:
            tag_type_list = [TagType.from_text(text=value) for value in tag]
            _tag = Tag(kind_types=TagTypes(values=tag_type_list))
            properties.append(_tag)

        if date_:
            _date = Date.from_start_date(start_date=date_)
            properties.append(_date)

        return AccountBook(properties=Properties(values=properties))
