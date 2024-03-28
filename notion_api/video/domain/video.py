from dataclasses import dataclass

from common.domain.tag_relation import TagRelation
from common.value.notion_page_id_list import NotionPageIdList
from notion_client_wrapper.base_page import BasePage
from notion_client_wrapper.block.block import Block
from notion_client_wrapper.properties.cover import Cover
from notion_client_wrapper.properties.properties import Properties
from video.domain.video_title import VideoName
from video.domain.video_url import VideoUrl


@dataclass
class Video(BasePage):
    @staticmethod
    def create(
            title: str|VideoName,
            url: str|VideoUrl,
            tag_relation: list[str]|TagRelation|None = None,
            blocks: list[Block]|None = None,
            cover: str|Cover|None = None) -> "Video":
        blocks = blocks or []
        properties = [
            title if isinstance(title, VideoName) else VideoName(text=title),
            url if isinstance(url, VideoUrl) else VideoUrl(url=url),
        ]
        if tag_relation is not None:
            if isinstance(tag_relation, TagRelation):
                properties.append(tag_relation)
            else:
              properties.append(TagRelation.from_id_list(id_list=tag_relation))

        if cover is None:
            return Video(properties=Properties(values=properties), block_children=blocks)
        cover = cover if isinstance(cover, Cover) else Cover.from_external_url(cover)
        return Video(properties=Properties(values=properties), block_children=blocks, cover=cover)

    @property
    def video_name(self) -> str:
        return self.get_title_text()

    @property
    def video_url(self) -> str:
        return self.get_url(name=VideoUrl.NAME).url

    @property
    def tag_relation(self) -> NotionPageIdList:
        id_list = self.get_relation(TagRelation.NAME).id_list
        return NotionPageIdList.from_str_list(id_list)
