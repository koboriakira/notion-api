from logging import Logger, getLogger

from notion_client_wrapper.block.bulleted_list_item import BulletedlistItem
from lotion import Lotion
from lotion.page import PageId
from project.domain.project import Project
from project.domain.project_repository import ProjectRepository
from task.domain.task_repository import TaskRepository
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

    def execute(self, project_template_id: PageId) -> Project:
        base_page = self._client.retrieve_page(page_id=project_template_id.value)
        project_name = base_page.get_text(name="プロジェクト名").text
        task_list: list[str] = []
        for block in base_page.block_children:
            if isinstance(block, BulletedlistItem):
                task_list.append(block.rich_text.to_plain_text())

        return self._create_project_service.execute(
            project_name=project_name,
            tasks_request=[{"title": task} for task in task_list],
        )
