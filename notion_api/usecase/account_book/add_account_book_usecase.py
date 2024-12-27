from datetime import date

from lotion import Lotion
from lotion.properties import Properties

from account_book.domain.account_book import AccountBook, AccountDate, AccountTitle, Category, IsFixedCost, Price, Tag
from account_book.domain.category import CategoryType
from account_book.domain.tag import TagType, TagTypes


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
    ) -> dict[str, str]:
        account_book = self._create_entity(
            title=title,
            price=price,
            is_fixed_cost=is_fixed_cost,
            category=category,
            tag=tag,
            date_=date_,
        )
        return self._save(account_book).get_id_and_url()

    def _save(self, entity: AccountBook) -> AccountBook:
        """Save a AccountBook item."""
        # FIXME: `update`で自動的に作成or更新するようにしたい
        if entity.is_created():
            self._lotion.update_page(page_id=entity.id, properties=entity.properties.values)
            return entity
        return self._lotion.create_page(entity)

    def _create_entity(  # noqa: PLR0913
        self,
        title: str,
        price: int,
        is_fixed_cost: bool | None = None,
        category: str | None = None,
        tag: list[str] | None = None,
        date_: date | None = None,
    ) -> AccountBook:
        properties = []

        properties.append(AccountTitle.from_plain_text(text=title))
        properties.append(Price.from_num(value=price))

        if is_fixed_cost:
            properties.append(IsFixedCost.true())

        if category:
            category_type = CategoryType.from_text(text=category)
            _category = Category(
                name=Category.PROP_NAME,
                selected_name=category_type.selected_name,
                selected_id=category_type.selected_id,
                selected_color=category_type.selected_color,
                id=None,
            )
            properties.append(_category)

        if tag and len(tag) > 0:
            tag_type_list = TagTypes([TagType.from_text(text=value) for value in tag])
            _tag = Tag(
                name=Tag.PROP_NAME,
                values=tag_type_list.to_multi_select_elements(),
            )
            properties.append(_tag)

        if date_:
            properties.append(AccountDate.from_start_date(start_date=date_))

        return AccountBook(properties=Properties(values=properties))
