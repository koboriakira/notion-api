from logging import Logger

from common.value.database_type import DatabaseType
from custom_logger import get_logger
from notion_client_wrapper.client_wrapper import ClientWrapper

logger = get_logger(__name__)

database_list = [
    DatabaseType.TASK,
    DatabaseType.PROJECT,
    DatabaseType.BOOK,
    DatabaseType.WEBCLIP,
    DatabaseType.PROWRESTLING,
    DatabaseType.RECIPE,
    DatabaseType.VIDEO,
    DatabaseType.MUSIC,
]


class CleanEmptyTitlePageUsecase:
    def __init__(self, client: ClientWrapper, logger: Logger | None = None) -> None:
        self.client = client
        self._logger = logger or get_logger(__name__)

    def handle(self) -> dict:
        for database in database_list:
            self._clean(database=database)

    def _clean(self, database: DatabaseType) -> None:
        self._logger.info(f"Start clean empty title page: {database}")
        pages = self.client.retrieve_database(database_id=database.value)
        self._logger.info(f"length of page: {len(pages)}")
        for page in pages:
            if page.get_title_text() == "":
                self._logger.info(f"Remove empty title page_id: {page.id}")
                self.client.remove_page(page_id=page.id)


if __name__ == "__main__":
    # python -m usecase.clean_empty_title_page
    usecase = CleanEmptyTitlePageUsecase()
    usecase.handle()
