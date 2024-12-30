from lotion import notion_database, notion_prop
from lotion.base_page import BasePage
from lotion.block import Block
from lotion.properties import Cover, Property, Title, Url

from common.domain.tag_relation import TagRelation
from common.value.database_type import DatabaseType


@notion_prop("名前")
class RestaurantName(Title):
    pass


@notion_prop("URL")
class RestaurantUrl(Url):
    pass


@notion_database(DatabaseType.RESTAURANT.value)
class Restaurant(BasePage):
    name: RestaurantName
    url: RestaurantUrl
    tags: TagRelation

    @staticmethod
    def generate(
        title: str,
        url: str,
        tag_relation: list[str] | None = None,
        blocks: list[Block] | None = None,
        cover: str | None = None,
    ) -> "Restaurant":
        blocks = blocks or []
        properties: list[Property] = [
            RestaurantName.from_plain_text(title),
            RestaurantUrl.from_url(url),
        ]
        if tag_relation is not None:
            properties.append(TagRelation.from_id_list(tag_relation))

        if cover is None:
            return Restaurant.create(properties, blocks)
        return Restaurant.create(properties, blocks, cover=Cover.from_external_url(cover))
