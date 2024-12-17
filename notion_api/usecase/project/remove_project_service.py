from custom_logger import get_logger
from lotion.page.page_id import PageId
from project.domain.project_repository import ProjectRepository
from task.domain.task_repository import TaskRepository

logger = get_logger(__name__)


class RemoveProjectService:
    def __init__(self, task_repository: TaskRepository, project_repository: ProjectRepository) -> None:
        self._task_repository = task_repository
        self._project_repository = project_repository

    def execute(self, id_: PageId) -> None:
        project = self._project_repository.find_by_id(page_id=id_.value)

        tasks = self._task_repository.search(project_id=id_)
        for task in tasks:
            self._task_repository.delete(task)

        self._project_repository.remove(project)
