from dataclasses import dataclass

from common.domain.tag_relation import TagRelation
from common.value.notion_page_id_list import NotionPageIdList
from notion_client_wrapper.base_page import BasePage
from notion_client_wrapper.block.block import Block
from notion_client_wrapper.properties.cover import Cover
from notion_client_wrapper.properties.properties import Properties
from zettlekasten.domain.reference_url import ReferenceUrl
from zettlekasten.domain.zettlekasten_title import ZettlekastenName


@dataclass
class Zettlekasten(BasePage):
    @staticmethod
    def create(
        title: str | ZettlekastenName,
        reference_url: str | ReferenceUrl | None = None,
        tag_relation: list[str] | TagRelation | None = None,
        blocks: list[Block] | None = None,
        cover: str | Cover | None = None,
    ) -> "Zettlekasten":
        blocks = blocks or []
        properties = [
            title if isinstance(title, ZettlekastenName) else ZettlekastenName(text=title),
            reference_url if isinstance(reference_url, ReferenceUrl) else ReferenceUrl(url=reference_url),
        ]
        if tag_relation is not None:
            if isinstance(tag_relation, TagRelation):
                properties.append(tag_relation)
            else:
                properties.append(TagRelation.from_id_list(id_list=tag_relation))

        if cover is None:
            return Zettlekasten(properties=Properties(values=properties), block_children=blocks)
        cover = cover if isinstance(cover, Cover) else Cover.from_external_url(cover)
        return Zettlekasten(properties=Properties(values=properties), block_children=blocks, cover=cover)

    def update_tag_relation(self, tag_relation: TagRelation) -> None:
        properties = self.properties.append_property(tag_relation)
        self.properties = properties

    @property
    def zettlekasten_name(self) -> str:
        return self.get_title_text()

    @property
    def reference_url(self) -> str:
        return self.get_url(name=ReferenceUrl.NAME).url

    @property
    def tag_relation(self) -> NotionPageIdList:
        id_list = self.get_relation(TagRelation.NAME).id_list
        return NotionPageIdList.from_str_list(id_list)
