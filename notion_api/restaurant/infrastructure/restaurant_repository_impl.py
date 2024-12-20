from logging import Logger, getLogger

from lotion import Lotion
from lotion.base_page import BasePage
from lotion.filter import Builder
from lotion.filter.condition import Cond, Prop

from common.value.database_type import DatabaseType
from restaurant.domain.restaurant import Restaurant


class RestaurantRepositoryImpl:
    def __init__(self, client: Lotion, logger: Logger | None = None) -> None:
        self._client = client
        self._logger = logger or getLogger(__name__)

    def find_by_title(self, title: str) -> Restaurant | None:
        builder = Builder.create().add(Prop.RICH_TEXT, "名前", Cond.EQUALS, title)
        searched_restaurant = self._client.retrieve_database(
            database_id=DatabaseType.RESTAURANT.value,
            filter_param=builder.build(),
        )
        if len(searched_restaurant) == 0:
            return None
        if len(searched_restaurant) > 1:
            warning_message = f"Found multiple restaurant with the same title: {title}"
            self._logger.warning(warning_message)
        return self._cast(searched_restaurant[0])

    def save(self, restaurant: Restaurant) -> Restaurant:
        result = self._client.create_page_in_database(
            database_id=DatabaseType.RESTAURANT.value,
            properties=restaurant.properties.values,
        )
        restaurant.update_id_and_url(
            page_id=result.id,
            url=result.url,
        )
        return restaurant

    def _cast(self, base_page: BasePage) -> Restaurant:
        return Restaurant(
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
