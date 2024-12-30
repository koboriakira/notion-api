from lotion import Lotion

from custom_logger import get_logger
from notion_databases.task import Task
from task.task_repository import TaskRepository


class TaskUtilService:
    def __init__(self, task_repository: TaskRepository, lotion: Lotion | None = None) -> None:
        self._task_repository = task_repository
        self._lotion = lotion or Lotion.get_instance()
        self._logger = get_logger(__name__)

    def start(self, page_id: str) -> None:
        """
        Start the task.
        """
        task = self._find_task(page_id)
        self._task_repository.save(task.start())

    def postpone(self, page_id: str, days: int) -> None:
        """
        Postpone the task.
        """
        task = self._find_task(page_id)
        self._task_repository.save(task.do_tomorrow())

    def complete(self, page_id: str) -> None:
        """
        Complete the task.
        """
        task = self._find_task(page_id)
        self._task_repository.save(task.complete())

    def _find_task(self, page_id: str) -> Task:
        task = self._task_repository.find_by_id(task_id=page_id)
        if task is None:
            msg = f"Task not found. page_id={page_id}"
            raise ValueError(msg)
        return task
