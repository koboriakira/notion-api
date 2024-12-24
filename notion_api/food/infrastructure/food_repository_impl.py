from logging import Logger, getLogger

from lotion import Lotion
from lotion.base_page import BasePage
from lotion.filter import Builder, Cond, Prop

from common.value.database_type import DatabaseType
from food.domain.food import Food
from food.domain.food_repository import FoodRepository


class FoodRepositoryImpl(FoodRepository):
    DATABASE_ID = DatabaseType.FOOD.value

    def __init__(self, client: Lotion, logger: Logger | None = None) -> None:
        self._client = client
        self._logger = logger or getLogger(__name__)

    def find_by_title(self, title: str) -> Food | None:
        builder = Builder.create().add(Prop.RICH_TEXT, "名前", Cond.EQUALS, title)
        searched_food = self._client.retrieve_database(
            database_id=self.DATABASE_ID,
            filter_param=builder.build(),
        )
        if len(searched_food) == 0:
            return None
        if len(searched_food) > 1:
            warning_message = f"Found multiple food with the same title: {title}"
            self._logger.warning(warning_message)
        return self._cast(searched_food[0])

    def save(self, food: Food) -> Food:
        result = self._client.create_page_in_database(
            database_id=self.DATABASE_ID,
            properties=food.properties.values,
        )
        food.update_id_and_url(
            page_id=result.id,
            url=result.url,
        )
        return food

    def _cast(self, base_page: BasePage) -> Food:
        return Food(
            properties=base_page.properties,
            block_children=base_page.block_children,
            id_=base_page.id_,
            url_=base_page.url,
            created_time=base_page.created_time,
            last_edited_time=base_page.last_edited_time,
            _created_by=base_page._created_by,
            _last_edited_by=base_page._last_edited_by,
            cover=base_page.cover,
            icon=base_page.icon,
            archived=base_page.archived,
            parent=base_page.parent,
        )
