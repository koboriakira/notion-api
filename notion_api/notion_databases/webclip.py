from lotion import notion_database, notion_prop
from lotion.base_page import BasePage
from lotion.block import Block
from lotion.properties import Cover, Property, Status, Text, Title, Url

from common.domain.tag_relation import TagRelation

COLUMN_NAME_TITLE = "名前"


@notion_prop("名前")
class WebClipTitle(Title):
    pass


@notion_prop("URL")
class WebClipUrl(Url):
    pass


@notion_prop("ステータス")
class WebClipStatus(Status):
    pass


@notion_prop("概要")
class Summary(Text):
    pass


@notion_database("b5e701d7-75d0-4355-8c59-dc3e2f0c09ac")
class Webclip(BasePage):
    title: WebClipTitle
    status: WebClipStatus
    tags: TagRelation
    clipped_url: WebClipUrl
    summary: Summary

    @staticmethod
    def generate(  # noqa: PLR0913
        title: str,
        url: str,
        tag_relation: list[str] | None = None,
        summary: str | None = None,
        blocks: list[Block] | None = None,
        cover: str | None = None,
    ) -> "Webclip":
        blocks = blocks or []
        properties: list[Property] = [
            WebClipTitle.from_plain_text(title),
            WebClipUrl.from_url(url),
        ]
        if tag_relation is not None:
            properties.append(TagRelation.from_id_list(tag_relation))
        if summary is not None:
            properties.append(Summary.from_plain_text(summary))

        if cover is None:
            return Webclip.create(properties, blocks)
        return Webclip.create(properties, blocks, cover=Cover.from_external_url(cover))
