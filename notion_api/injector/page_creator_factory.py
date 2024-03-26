

from logging import Logger

from common.service.page_creator import NotImplementPageCreator, PageCreator
from common.value.site_kind import SiteKind
from notion_client_wrapper.client_wrapper import ClientWrapper
from restaurant.infrastructure.restaurant_repository_impl import RestaurantRepositoryImpl
from restaurant.service.restaurant_creator import RestaurantCreator


class PageCreatorFactory:
    def __init__(self, generator_dict: dict[SiteKind, PageCreator]) -> None:
        self.generator_dict = generator_dict

    @staticmethod
    def generate_rule(logger: Logger) -> "PageCreatorFactory":
        client = ClientWrapper.get_instance()
        restaurant_repository = RestaurantRepositoryImpl(client=client)

        generator_dict = {}
        for site_kind in SiteKind:
            match site_kind:
                case SiteKind.TABELOG:
                    generator_dict[site_kind] = RestaurantCreator(
                        restaurant_repository=restaurant_repository,
                        logger=logger,
                        )
                case _:
                    generator_dict[site_kind] = NotImplementPageCreator()
        return PageCreatorFactory(generator_dict=generator_dict)

    def get_creator(self, site_kind: SiteKind) -> PageCreator:
        """任意のPageCreatorを取得する"""
        return self.generator_dict[site_kind]
