from logging import Logger, getLogger

from lotion import Lotion
from lotion.properties import Date, Property

from common.value.database_type import DatabaseType
from notion_databases.project import Project
from project.project_repository import ProjectRepository


class ProjectRepositoryImpl(ProjectRepository):
    DATABASE_ID = DatabaseType.PROJECT.value

    def __init__(self, client: Lotion | None = None, logger: Logger | None = None) -> None:
        self._client = client or Lotion.get_instance()
        self._logger = logger or getLogger(__name__)

    def fetch_all(self) -> list[Project]:
        return self._client.retrieve_pages(Project)

    def archive(self, project: Project) -> None:
        if not project.is_created():
            raise ValueError("Project is not created")

        properties: list[Property] = [
            project.title,
            Date.from_start_date(name="完了日", start_date=project.last_edited_time),
            project.goal,
            project.tags,
        ]

        _ = self._client.create_page_in_database(
            database_id=DatabaseType.PROJECT_BK.value,
            properties=properties,
            blocks=project.block_children,
        )

        self.remove(project)

    def save(self, project: Project) -> "Project":
        return self._client.update(project)

    def find_by_id(self, page_id: str) -> Project:
        return self._client.retrieve_page(page_id=page_id, cls=Project)

    def remove(self, project: Project) -> None:
        if not project.is_created():
            raise ValueError("Project is not created")
        self._client.remove_page(project.id)
