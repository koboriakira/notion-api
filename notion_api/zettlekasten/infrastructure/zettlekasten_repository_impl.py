from logging import Logger, getLogger

from lotion import Lotion
from lotion.base_page import BasePage
from lotion.filter import Builder
from lotion.filter.condition import Cond, Prop

from common.domain.tag_relation import TagRelation
from common.value.database_type import DatabaseType
from zettlekasten.domain.zettlekasten import Zettlekasten
from zettlekasten.domain.zettlekasten_repository import ZettlekastenRepository


class ZettlekastenRepositoryImpl(ZettlekastenRepository):
    DATABASE_ID = DatabaseType.ZETTLEKASTEN.value

    def __init__(self, client: Lotion, logger: Logger | None = None) -> None:
        self._client = client
        self._logger = logger or getLogger(__name__)

    def fetch_all(self) -> list[Zettlekasten]:
        base_pages = self._client.retrieve_database(
            database_id=self.DATABASE_ID,
        )
        return [self._cast(page) for page in base_pages]

    def search(
        self,
        is_tag_empty: bool | None = None,
        include_children: bool | None = None,
    ) -> list[Zettlekasten]:
        builder = Builder.create()
        if is_tag_empty is not None:
            builder = builder.add(Prop.RELATION, TagRelation.NAME, Cond.IS_EMPTY, True)
        filter_param = builder.build()
        base_pages = self._client.retrieve_database(
            database_id=self.DATABASE_ID,
            filter_param=filter_param,
            include_children=include_children,
        )
        return [self._cast(page) for page in base_pages]

    def find_by_title(self, title: str) -> Zettlekasten | None:
        builder = Builder.create().add(Prop.RICH_TEXT, "名前", Cond.EQUALS, title)
        searched_zettlekasten = self._client.retrieve_database(
            database_id=self.DATABASE_ID,
            filter_param=builder.build(),
            include_children=True,
        )
        if len(searched_zettlekasten) == 0:
            return None
        if len(searched_zettlekasten) > 1:
            warning_message = f"Found multiple zettlekasten with the same title: {title}"
            self._logger.warning(warning_message)
        return self._cast(searched_zettlekasten[0])

    def save(self, zettlekasten: Zettlekasten) -> Zettlekasten:
        if zettlekasten.id is not None:
            _ = self._client.update_page(page_id=zettlekasten.id, properties=zettlekasten.properties.values)
            return zettlekasten
        result = self._client.create_page_in_database(
            database_id=self.DATABASE_ID,
            cover=zettlekasten.cover,
            properties=zettlekasten.properties.values,
        )
        zettlekasten.update_id_and_url(
            page_id=result.page_id.value,
            url=result.url,
        )
        return zettlekasten

    def _cast(self, base_page: BasePage) -> Zettlekasten:
        return Zettlekasten(
            properties=base_page.properties,
            block_children=base_page.block_children,
            id_=base_page.id_,
            url=base_page.url,
            created_time=base_page.created_time,
            last_edited_time=base_page.last_edited_time,
            _created_by=base_page._created_by,
            _last_edited_by=base_page._last_edited_by,
            cover=base_page.cover,
            icon=base_page.icon,
            archived=base_page.archived,
            parent=base_page.parent,
        )
