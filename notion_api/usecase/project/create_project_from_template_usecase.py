from logging import Logger, getLogger

from lotion import Lotion
from lotion.block import BulletedListItem

from notion_databases.project import Project
from project.project_repository import ProjectRepository
from task.task_repository import TaskRepository
from usecase.project.create_project_service import CreateProjectService, TaskRequest, TaskRequestTitle


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
        self._create_project_service = CreateProjectService()
        self._logger = logger or getLogger(__name__)

    def execute(self, project_template_id: str) -> Project:
        base_page = self._client.retrieve_page(page_id=project_template_id)
        project_name = base_page.get_text(name="プロジェクト名").text
        task_text_list = [b.rich_text for b in base_page.block_children if isinstance(b, BulletedListItem)]

        return self._create_project_service.execute(
            project_name=project_name,
            tasks_request=[TaskRequest(title=TaskRequestTitle(value=task_text)) for task_text in task_text_list],
        )


if __name__ == "__main__":
    # python -m notion_api.usecase.project.create_project_from_template_usecase
    from notion_api.project.project_repository_impl import ProjectRepositoryImpl
    from notion_api.task.task_repository_impl import TaskRepositoryImpl

    client = Lotion.get_instance()
    project_repository = ProjectRepositoryImpl(client)
    task_repository = TaskRepositoryImpl(client)
    usecase = CreateProjectFromTemplateUsecase(client, project_repository, task_repository)
    usecase.execute("1706567a3bbf80caab25f447724b8dd1")
