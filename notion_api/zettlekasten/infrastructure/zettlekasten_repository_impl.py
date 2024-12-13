from logging import Logger, getLogger

from common.domain.tag_relation import TagRelation
from common.value.database_type import DatabaseType
from lotion import Lotion
from notion_client_wrapper.filter.condition.empty_condition import EmptyCondition
from notion_client_wrapper.filter.filter_builder import FilterBuilder
from zettlekasten.domain.zettlekasten import Zettlekasten
from zettlekasten.domain.zettlekasten_repository import ZettlekastenRepository
from zettlekasten.domain.zettlekasten_title import ZettlekastenName


class ZettlekastenRepositoryImpl(ZettlekastenRepository):
    DATABASE_ID = DatabaseType.ZETTLEKASTEN.value

    def __init__(self, client: Lotion, logger: Logger | None = None) -> None:
        self._client = client
        self._logger = logger or getLogger(__name__)

    def fetch_all(self) -> list[Zettlekasten]:
        return self._client.retrieve_database(
            database_id=self.DATABASE_ID,
            page_model=Zettlekasten,
        )

    def search(
        self,
        is_tag_empty: bool | None = None,
        include_children: bool | None = None,
    ) -> list[Zettlekasten]:
        filter_builder = FilterBuilder()
        if is_tag_empty is not None:
            filter_builder = filter_builder.add_condition(
                EmptyCondition.true(prop_name=TagRelation.NAME, prop_type=TagRelation.TYPE),
            )
        filter_param = filter_builder.build()
        return self._client.retrieve_database(
            database_id=self.DATABASE_ID,
            filter_param=filter_param,
            page_model=Zettlekasten,
            include_children=include_children,
        )

    def find_by_title(self, title: str) -> Zettlekasten | None:
        title_property = ZettlekastenName(text=title)
        filter_param = FilterBuilder.build_simple_equal_condition(title_property)
        searched_zettlekasten = self._client.retrieve_database(
            database_id=self.DATABASE_ID,
            filter_param=filter_param,
            page_model=Zettlekasten,
            include_children=True,
        )
        if len(searched_zettlekasten) == 0:
            return None
        if len(searched_zettlekasten) > 1:
            warning_message = f"Found multiple zettlekasten with the same title: {title}"
            self._logger.warning(warning_message)
        return searched_zettlekasten[0]

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
            page_id=result["id"],
            url=result["url"],
        )
        return zettlekasten
