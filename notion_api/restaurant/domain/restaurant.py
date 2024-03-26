from dataclasses import dataclass

from common.domain.tag_relation import TagRelation
from common.value.notion_page_id_list import NotionPageIdList
from notion_client_wrapper.base_page import BasePage
from notion_client_wrapper.block.block import Block
from notion_client_wrapper.properties.cover import Cover
from notion_client_wrapper.properties.properties import Properties
from restaurant.domain.restaurant_title import RestaurantName
from restaurant.domain.restaurant_url import RestaurantUrl


@dataclass
class Restaurant(BasePage):
    @staticmethod
    def create(
            title: str|RestaurantName,
            url: str|RestaurantUrl,
            tag_relation: list[str]|TagRelation|None = None,
            blocks: list[Block]|None = None,
            cover: str|Cover|None = None) -> "Restaurant":
        blocks = blocks or []
        properties = [
            title if isinstance(title, RestaurantName) else RestaurantName(text=title),
            url if isinstance(url, RestaurantUrl) else RestaurantUrl(url=url),
        ]
        if tag_relation is not None:
            if isinstance(tag_relation, TagRelation):
                properties.append(tag_relation)
            else:
              properties.append(TagRelation.from_id_list(id_list=tag_relation))

        if cover is None:
            return Restaurant(properties=Properties(values=properties), block_children=blocks)
        cover = cover if isinstance(cover, Cover) else Cover.from_external_url(cover)
        return Restaurant(properties=Properties(values=properties), block_children=blocks, cover=cover)

    @property
    def restaurant_name(self) -> str:
        return self.get_title_text()

    @property
    def restaurant_url(self) -> str:
        return self.get_url(name=RestaurantUrl.NAME).url

    @property
    def tag_relation(self) -> NotionPageIdList:
        id_list = self.get_relation(TagRelation.NAME).id_list
        return NotionPageIdList.from_str_list(id_list)

    def update_id_and_url(self, page_id: str, url: str) -> None:
        self.id = page_id
        self.url = url
