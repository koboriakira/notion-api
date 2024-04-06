from logging import Logger, getLogger

from domain.database_type import DatabaseType
from notion_client_wrapper.client_wrapper import ClientWrapper
from project.domain.project import Project
from project.domain.project_repository import ProjectRepository


class ProjectRepositoryImpl(ProjectRepository):
    def __init__(self, client: ClientWrapper, logger: Logger | None = None) -> None:
        self._client = client
        self._logger = logger or getLogger(__name__)

    def fetch_all(self) -> list[Project]:
        return self._client.retrieve_database(database_id=DatabaseType.PROJECT.value, page_model=Project)
