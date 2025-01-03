from logging import Logger, getLogger

from lotion import Lotion
from lotion.block import BulletedListItem

from notion_databases.project import Project
from project.project_repository import ProjectRepository
from task.task_repository import TaskRepository
from usecase.project.create_project_service import CreateProjectService


class CreateProjectFromTemplateUsecase:
    def __init__(
        self,
        client: Lotion,
        project_repository: ProjectRepository,
        task_repository: TaskRepository,
        logger: Logger | None = None,
    ) -> None:
        self._client = client
        self._project_repository = project_repository
        self._task_repository = task_repository
        self._create_project_service = CreateProjectService(
            task_repository=task_repository,
            project_repository=project_repository,
        )
        self._logger = logger or getLogger(__name__)

    def execute(self, project_template_id: str) -> Project:
        base_page = self._client.retrieve_page(page_id=project_template_id)
        project_name = base_page.get_text(name="プロジェクト名").text
        task_list: list[str] = []
        for block in base_page.block_children:
            if isinstance(block, BulletedListItem):
                task_list.append(block.rich_text.to_plain_text())

        return self._create_project_service.execute(
            project_name=project_name,
            tasks_request=[{"title": task} for task in task_list],
        )
