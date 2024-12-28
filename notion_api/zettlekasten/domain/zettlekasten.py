from lotion import notion_database, notion_prop
from lotion.base_page import BasePage
from lotion.block import Block
from lotion.properties import Cover, Property, Title, Url

from common.domain.tag_relation import TagRelation
from common.value.database_type import DatabaseType


@notion_prop("記事")
class ReferenceUrl(Url):
    pass


@notion_prop("名前")
class ZettlekastenName(Title):
    pass


@notion_database(DatabaseType.ZETTLEKASTEN.value)
class Zettlekasten(BasePage):
    title: ZettlekastenName
    reference_url: ReferenceUrl
    tags: TagRelation

    @staticmethod
    def generate(
        title: str,
        reference_url: str | None = None,
        tag_relation: list[str] | None = None,
        blocks: list[Block] | None = None,
        cover: str | None = None,
    ) -> "Zettlekasten":
        blocks = blocks or []
        properties: list[Property] = []
        properties.append(ZettlekastenName.from_plain_text(title))
        if reference_url is not None:
            properties.append(ReferenceUrl.from_url(reference_url))
        if tag_relation is not None:
            properties.append(TagRelation.from_id_list(tag_relation))

        if cover is None:
            return Zettlekasten.create(properties, blocks)
        return Zettlekasten.create(
            properties,
            blocks,
            cover=Cover.from_external_url(cover),
        )
