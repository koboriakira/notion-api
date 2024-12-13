from dataclasses import dataclass

from common.domain.tag_relation import TagRelation
from common.value.notion_page_id_list import NotionPageIdList
from lotion.base_page import BasePage
from notion_client_wrapper.block.block import Block
from lotion.properties import Cover
from lotion.properties import Properties
from video.domain.video_title import VideoName
from video.domain.video_url import VideoUrl

EMBED_YOUTUBE_URL_TEMPLATE = """<iframe width="560" height="315" src="https://www.youtube.com/embed/%s" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>"""

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

    @property
    def embed_youtube_url(self) -> str:
        # https://www.youtube.com/watch?v=sVegt6PdQOw&amp%3Bsi=M7Z4IT0tpe__8ap9 から sVegt6PdQOw を取り出す
        url = self.video_url
        video_id = url.split("v=")[1].split("&")[0]
        return EMBED_YOUTUBE_URL_TEMPLATE % video_id
