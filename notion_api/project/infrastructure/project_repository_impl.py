from logging import Logger, getLogger

from common.domain.tag_relation import TagRelation
from common.value.database_type import DatabaseType
from notion_client_wrapper.base_page import BasePage
from notion_client_wrapper.client_wrapper import ClientWrapper
from notion_client_wrapper.properties.date import Date
from notion_client_wrapper.properties.property import Property
from project.domain.goal_relation import GoalRelation
from project.domain.project import Project
from project.domain.project_repository import ProjectRepository


class ProjectRepositoryImpl(ProjectRepository):
    def __init__(self, client: ClientWrapper, logger: Logger | None = None) -> None:
        self._client = client
        self._logger = logger or getLogger(__name__)

    def fetch_all(self) -> list[Project]:
        base_pages = self._client.retrieve_database(database_id=DatabaseType.PROJECT.value)
        return [self._cast(base_page) for base_page in base_pages]

    def archive(self, project: Project) -> None:
        if project.id is None:
            raise ValueError("Project id is None")

        properties: list[Property] = [
            project.get_title(),
            Date.from_start_date(name="完了日", start_date=project.last_edited_time.date), # type: ignore
        ] # type: ignore
        if project.get_relation(GoalRelation.NAME) is not None:
            properties.append(project.get_relation(GoalRelation.NAME))
        if project.get_relation(TagRelation.NAME) is not None:
            properties.append(project.get_relation(TagRelation.NAME))

        self._client.create_page_in_database(
            database_id=DatabaseType.PROJECT_BK.value,
            properties=properties,
            blocks=project.block_children,
        )

        self.remove(project)

    def remove(self, project: Project) -> None:
        if project.id is None:
            raise ValueError("Project id is None")
        self._client.remove_page(page_id=project.id)

    def _cast(self, base_page: BasePage) -> Project:
        return Project(
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
