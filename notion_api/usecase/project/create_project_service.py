from custom_logger import get_logger
from project.domain.project import Project
from project.domain.project_repository import ProjectRepository
from project.domain.project_status import ProjectStatusType
from task.domain.task_kind import TaskKindType
from task.domain.task_repository import TaskRepository
from task.task_factory import TaskFactory

logger = get_logger(__name__)


class CreateProjectService:
    def __init__(self, task_repository: TaskRepository, project_repository: ProjectRepository) -> None:
        self._task_repository = task_repository
        self._project_repository = project_repository

    def execute(self, project_name: str, tasks_request: list[dict]) -> Project:
        project = self._project_repository.save(
            Project.create(
                title=project_name,
                project_status=ProjectStatusType.IN_PROGRESS,
            ),
        )
        for task_req in tasks_request:
            task_title = task_req["title"]
            task = TaskFactory.create_todo_task(
                title=task_title,
                task_kind_type=TaskKindType.NEXT_ACTION,
                project_id=project.id,
            )
            self._task_repository.save(task)
        return project
