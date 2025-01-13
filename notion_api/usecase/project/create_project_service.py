from lotion import Lotion
from lotion.block.rich_text import RichText

from custom_logger import get_logger
from notion_databases.project import Project
from notion_databases.project_prop.project_status import ProjectStatusType
from project.project_repository import ProjectRepository
from task.task_factory import TaskFactory
from task.task_repository import TaskRepository

logger = get_logger(__name__)


class CreateProjectService:
    def __init__(self, task_repository: TaskRepository, project_repository: ProjectRepository) -> None:
        self._lotion = Lotion.get_instance()
        self._task_repository = task_repository
        self._project_repository = project_repository

    def execute(self, project_name: str, tasks_request: list[dict[str, RichText]]) -> Project:
        print("CreateProjectService.execute")

        project = self._lotion.create_page(
            Project.generate(
                title=project_name,
                project_status=ProjectStatusType.IN_PROGRESS,
            ),
        )
        for task_req in tasks_request:
            title_rich_text = task_req["title_rich_text"]
            task = TaskFactory.create_todo_task(
                title=title_rich_text,
                project_id=project.id,
            )
            self._lotion.create_page(task)
        return project
