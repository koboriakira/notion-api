from dataclasses import dataclass

from common.domain.tag_relation import TagRelation
from notion_client_wrapper.base_page import BasePage
from notion_client_wrapper.block.block import Block
from notion_client_wrapper.properties.cover import Cover
from notion_client_wrapper.properties.properties import Properties
from notion_client_wrapper.properties.title import Title
from notion_client_wrapper.properties.url import Url
from webclip.domain.summary import Summary

COLUMN_NAME_TITLE = "名前"


@dataclass
class Webclip(BasePage):
    @staticmethod
    def create(
            title: str|Title,
            url: str|Url,
            tag_relation: list[str]|TagRelation|None = None,
            summary: str|Summary|None = None,
            blocks: list[Block]|None = None,
            cover: str|Cover|None = None) -> "Webclip":
        blocks = blocks or []
        properties = [
            title if isinstance(title, Title) else Title.from_plain_text(name=COLUMN_NAME_TITLE, text=title),
            url if isinstance(url, Url) else Url.from_url(name="URL", url=url),
        ]
        if tag_relation is not None:
            if isinstance(tag_relation, TagRelation):
                properties.append(tag_relation)
            else:
              properties.append(TagRelation.from_id_list(id_list=tag_relation))
        if summary is not None:
            if isinstance(summary, Summary):
                properties.append(summary)
            else:
                properties.append(Summary(text=summary))

        if cover is None:
            return Webclip(properties=Properties(values=properties), block_children=blocks)
        cover = cover if isinstance(cover, Cover) else Cover.from_external_url(cover)
        return Webclip(properties=Properties(values=properties), block_children=blocks, cover=cover)
