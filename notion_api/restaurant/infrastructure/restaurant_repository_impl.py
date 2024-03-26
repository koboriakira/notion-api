from logging import Logger, getLogger

from notion_client_wrapper.client_wrapper import ClientWrapper
from notion_client_wrapper.database.database_type import DatabaseType
from notion_client_wrapper.filter.filter_builder import FilterBuilder
from restaurant.domain.restaurant import Restaurant
from restaurant.domain.restaurant_title import RestaurantName


class RestaurantRepositoryImpl:
    def __init__(
            self,
            client: ClientWrapper,
            logger: Logger|None = None) -> None :
        self._client = client
        self._logger = logger or getLogger(__name__)

    def find_by_title(self, title: str) -> Restaurant|None:
        title_property = RestaurantName(text=title)
        filter_param = FilterBuilder.build_simple_equal_condition(title_property)
        searched_restaurant = self._client.retrieve_database(
            database_id=DatabaseType.RESTAURANT.value,
            filter_param=filter_param,
            page_model=Restaurant,
        )
        if len(searched_restaurant) == 0:
            return None
        if len(searched_restaurant) > 1:
            warning_message = f"Found multiple restaurant with the same title: {title}"
            self._logger.warning(warning_message)
        return searched_restaurant[0]

    def save(self, restaurant: Restaurant) -> Restaurant:
        result = self._client.create_page_in_database(
            database_id=DatabaseType.RESTAURANT.value,
            properties=restaurant.properties.values,
        )
        restaurant.update_id_and_url(
            page_id=result["id"],
            url=result["url"],
        )
        return restaurant
