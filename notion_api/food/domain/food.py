from dataclasses import dataclass

from notion_client_wrapper.base_page import BasePage
from notion_client_wrapper.block.block import Block
from notion_client_wrapper.properties.cover import Cover
from notion_client_wrapper.properties.properties import Properties
from notion_client_wrapper.properties.property import Property
from notion_client_wrapper.properties.title import Title


@dataclass
class Food(BasePage):
    @staticmethod
    def create(title: str, blocks: list[Block] | None = None, cover: str | Cover | None = None) -> "Food":
        blocks = blocks or []
        properties: list[Property] = [
            Title.from_plain_text(text=title),
        ]
        properties_ = Properties(properties)
        return Food(properties=properties_, block_children=blocks)
        # if cover is None:
        #     return Food(properties=Properties(values=properties), block_children=blocks)
        # cover = cover if isinstance(cover, Cover) else Cover.from_external_url(cover)
        # return Food(properties=Properties(values=properties), block_children=blocks, cover=cover)
