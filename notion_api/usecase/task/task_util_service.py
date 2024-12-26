from custom_logger import get_logger
from task.domain.task import Task
from task.domain.task_repository import TaskRepository


class TaskUtilService:
    def __init__(self, task_repository: TaskRepository) -> None:
        self._task_repository = task_repository
        self._logger = get_logger(__name__)

    def start(self, page_id: str) -> None:
        """
        Start the task.
        """
        task = self._find_task(page_id)
        self._task_repository.save(task.start())

    def _find_task(self, page_id: str) -> Task:
        task = self._task_repository.find_by_id(task_id=page_id)
        if task is None:
            msg = f"Task not found. page_id={page_id}"
            raise ValueError(msg)
        return task

