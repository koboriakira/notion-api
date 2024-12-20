from logging import Logger

from lotion import Lotion
from lotion.filter import Builder
from lotion.filter.condition import Cond, Prop

from common.value.database_type import DatabaseType
from custom_logger import get_logger

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
    def __init__(self, client: Lotion | None = None, logger: Logger | None = None) -> None:
        self._client = client or Lotion.get_instance()
        self._logger = logger or get_logger(__name__)

    def handle(self) -> None:
        for database in database_list:
            self._clean(database=database)

    def _clean(self, database: DatabaseType) -> None:
        self._logger.info(f"Start clean empty title page: {database}")
        pages = self._client.retrieve_database(
            database_id=database.value,
            filter_param=self._create_filter_param(),
        )
        self._logger.info(f"length of page: {len(pages)}")
        for page in pages:
            if page.get_title_text() == "":
                self._logger.info(f"Remove empty title page_id: {page.id}")
                self._client.remove_page(page_id=page.id)

    def _create_filter_param(self) -> dict:
        builder = Builder.create().add(Prop.RICH_TEXT, "名前", Cond.IS_EMPTY, True)
        return builder.build()


if __name__ == "__main__":
    # python -m notion_api.usecase.clean_empty_title_page

    usecase = CleanEmptyTitlePageUsecase()
    usecase.handle()
