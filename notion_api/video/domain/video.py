from lotion import notion_database, notion_prop
from lotion.base_page import BasePage
from lotion.block import Block
from lotion.properties import Cover, Title, Url

from common.domain.tag_relation import TagRelation
from common.value.database_type import DatabaseType

EMBED_YOUTUBE_URL_TEMPLATE = """<iframe width="560" height="315" src="https://www.youtube.com/embed/%s" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>"""


@notion_prop("名前")
class VideoName(Title):
    pass


@notion_prop("URL")
class VideoUrl(Url):
    pass


@notion_database(DatabaseType.VIDEO.value)
class Video(BasePage):
    title: VideoName
    url: VideoUrl
    tags: TagRelation

    @staticmethod
    def generate(
        title: str,
        url: str,
        tag_relation: list[str] | None = None,
        blocks: list[Block] | None = None,
        cover: str | None = None,
    ) -> "Video":
        blocks = blocks or []
        properties = [
            VideoName.from_plain_text(title),
            VideoUrl.from_url(url),
        ]
        if tag_relation is not None:
            properties.append(TagRelation.from_id_list(id_list=tag_relation))

        if cover is None:
            return Video.create(properties, blocks)
        return Video.create(properties, blocks, cover=Cover.from_external_url(cover))

    @property
    def embed_youtube_url(self) -> str:
        # https://www.youtube.com/watch?v=sVegt6PdQOw&amp%3Bsi=M7Z4IT0tpe__8ap9 から sVegt6PdQOw を取り出す
        url = self.url.url
        video_id = url.split("v=")[1].split("&")[0]
        return EMBED_YOUTUBE_URL_TEMPLATE % video_id
