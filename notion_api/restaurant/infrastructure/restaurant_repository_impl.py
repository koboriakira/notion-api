from logging import Logger, getLogger

from notion_client_wrapper.client_wrapper import ClientWrapper
from notion_client_wrapper.database.database_type import DatabaseType
from restaurant.domain.restaurant import Restaurant


class RestaurantRepositoryImpl:
    def __init__(
            self,
            client: ClientWrapper,
            logger: Logger|None = None) -> None :
        self._client = client
        self._logger = logger or getLogger(__name__)


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
