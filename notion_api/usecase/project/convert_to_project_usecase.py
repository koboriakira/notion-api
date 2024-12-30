from lotion import Lotion
from lotion.properties import Properties, Title

from custom_logger import get_logger
from notion_databases.project import Project
from project.project_repository import ProjectRepository

logger = get_logger(__name__)


class ConvertToProjectUsecase:
    def __init__(self, lotion: Lotion, project_repository: ProjectRepository) -> None:
        self._lotion = lotion
        self._project_repository = project_repository

    def execute(self, page_id: str, title: Title) -> Project:
        project = self._project_repository.save(Project(Properties([title]), block_children=[]))
        self._lotion.remove_page(page_id=page_id)
        return project
