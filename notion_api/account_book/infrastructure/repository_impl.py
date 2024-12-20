from logging import Logger, getLogger

from lotion import Lotion
from lotion.base_page import BasePage

from account_book.domain.account_book import AccountBook
from account_book.domain.repository import AccountRepository
from common.value.database_type import DatabaseType


class RepositoryImpl(AccountRepository):
    DATABASE_ID = DatabaseType.ACCOUNT_BOOK.value

    def __init__(self, client: Lotion, logger: Logger | None = None) -> None:
        self._client = client
        self._logger = logger or getLogger(__name__)

    def save(self, entity: AccountBook) -> AccountBook:
        """Save a AccountBook item."""
        if entity.id is not None:
            _ = self._client.update_page(page_id=entity.id, properties=entity.properties.values)
            return entity
        page = self._client.create_page_in_database(
            database_id=self.DATABASE_ID,
            properties=entity.properties.values,
            blocks=entity.block_children,
        )
        return self._find_by_id(page.id)

    def _find_by_id(self, page_id: str) -> AccountBook:
        base_page = self._client.retrieve_page(page_id=page_id)
        return self._cast(base_page)

    def _cast(self, base_page: BasePage) -> AccountBook:
        return AccountBook(
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
