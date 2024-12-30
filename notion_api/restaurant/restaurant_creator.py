from logging import Logger, getLogger

from common.injector import CommonInjector
from common.service.page_creator import PageCreator
from notion_databases.restaurant import Restaurant, RestaurantName


class RestaurantCreator(PageCreator):
    def __init__(
        self,
        logger: Logger | None = None,
    ) -> None:
        self._logger = logger or getLogger(__name__)
        self._scraper = CommonInjector.get_scrape_service()
        self._lotion = Lotion.get_instance()

    def execute(
        self,
        url: str,
        title: str | None = None,
        cover: str | None = None,
        params: dict | None = None,
    ) -> Restaurant:
        if title is None:
            msg = "title is required"
            raise ValueError(msg)

        info_message = f"{self.__class__} execute: url={url}, title={title}, cover={cover}"
        self._logger.info(info_message)

        restaurant = self._lotion.find_page(Restaurant, RestaurantName.from_plain_text(title))
        if restaurant is not None:
            info_message = f"Restaurant is already registered: {restaurant.name.text}"
            self._logger.info(info_message)
            return restaurant

        info_message = "Create a Restaurant"
        self._logger.info(info_message)

        # Restaurantを生成
        if cover is None:
            cover = self._scraper.execute(url=url).get_image_url()
        restaurant = Restaurant.generate(
            title=title,
            url=url,
            cover=cover,
        )

        return self._lotion.update(restaurant)


if __name__ == "__main__":
    # python -m notion_api.restaurant.service.restaurant_creator
    from lotion import Lotion

    client = Lotion.get_instance()
    suite = RestaurantCreator()
    suite.execute(
        url="https://tabelog.com/tokyo/A1316/A131604/13020181/",
        title="焼肉・光陽 (大崎/焼肉)",
    )
