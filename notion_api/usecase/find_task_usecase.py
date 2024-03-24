from custom_logger import get_logger
from domain.task.task import Task
from domain.task.task_repository import TaskRepository

logger = get_logger(__name__)

class FindTaskUsecase:
    def __init__(self, task_repository: TaskRepository) -> None:
        self._task_repository = task_repository


    def execute(self, task_id: str) -> Task:
        return self._task_repository.find_by_id(task_id=task_id)
