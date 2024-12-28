from lotion import notion_database, notion_prop
from lotion.base_page import BasePage
from lotion.block import Block
from lotion.properties import Cover, Property, Title

from common.value.database_type import DatabaseType


@notion_prop("名前")
class FoodName(Title):
    pass


@notion_database(DatabaseType.FOOD.value)
class Food(BasePage):
    name: FoodName

    @staticmethod
    def generate(title: str, blocks: list[Block] | None = None, cover: str | None = None) -> "Food":
        blocks = blocks or []
        properties: list[Property] = []
        properties.append(FoodName.from_plain_text(title))

        if cover is None:
            return Food.create(properties, blocks)
        return Food.create(properties, blocks, cover=Cover.from_external_url(cover))
