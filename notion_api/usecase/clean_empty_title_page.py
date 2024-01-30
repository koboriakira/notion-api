from notion_client_wrapper.client_wrapper import ClientWrapper
from domain.database_type import DatabaseType
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
    def __init__(self):
        self.client = ClientWrapper.get_instance()

    def handle(self) -> dict:
        for database in database_list:
            self._clean(database=database)

    def _clean(self, database: DatabaseType) -> None:
        pages = self.client.retrieve_database(database_id=database.value)
        for page in pages:
            if page.get_title().text == "":
                self.client.remove_page(page_id=page.id)

if __name__ == "__main__":
    # python -m usecase.clean_empty_title_page
    usecase = CleanEmptyTitlePageUsecase()
    usecase.handle()
