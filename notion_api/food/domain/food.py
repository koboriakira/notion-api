from dataclasses import dataclass

from lotion.base_page import BasePage
from lotion.block import Block
from lotion.properties import Cover, Properties, Property, Title


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
