from logging import Logger, getLogger

from common.value.database_type import DatabaseType
from notion_client_wrapper.base_page import BasePage
from lotion import Lotion
from notion_client_wrapper.page.page_id import PageId
from shopping.domain.repository import ShoppingRepository
from shopping.domain.shopping import Shopping


class ShoppingRepositoryImpl(ShoppingRepository):
    DATABASE_ID = DatabaseType.SHOPPING.value

    def __init__(self, client: Lotion, logger: Logger | None = None) -> None:
        self._client = client
        self._logger = logger or getLogger(__name__)

    def fetch_all(self) -> list[Shopping]:
        base_pages = self._client.retrieve_database(database_id=self.DATABASE_ID)
        return [self._cast(base_page) for base_page in base_pages]

    def save(self, entity: Shopping) -> Shopping:
        if entity.id is not None:
            _ = self._client.update_page(page_id=entity.id, properties=entity.properties.values)
            return entity
        page = self._client.create_page_in_database(
            database_id=self.DATABASE_ID,
            properties=entity.properties.values,
            blocks=entity.block_children,
        )
        return self._find_by_id(page["id"])

    def _find_by_id(self, shopping_page_id: PageId) -> "Shopping":
        base_page = self._client.retrieve_page(page_id=shopping_page_id.value)
        return self._cast(base_page)

    def _cast(self, base_page: BasePage) -> Shopping:
        return Shopping(
            properties=base_page.properties,
            block_children=base_page.block_children,
            id_=base_page.id_,
            url=base_page.url,
            created_time=base_page.created_time,
            last_edited_time=base_page.last_edited_time,
            created_by=base_page.created_by,
            last_edited_by=base_page.last_edited_by,
            cover=base_page.cover,
            icon=base_page.icon,
            archived=base_page.archived,
            parent=base_page.parent,
        )
