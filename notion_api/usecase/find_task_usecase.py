from custom_logger import get_logger
from notion_databases.task import Task
from task.domain.task_repository import TaskRepository

logger = get_logger(__name__)


class FindTaskUsecase:
    def __init__(self, task_repository: TaskRepository) -> None:
        self._task_repository = task_repository

    def execute(self, task_id: str) -> Task:
        return self._task_repository.find_by_id(task_id=task_id)
