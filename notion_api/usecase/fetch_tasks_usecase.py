from datetime import date

from custom_logger import get_logger
from domain.task.task import Task
from domain.task.task_repository import TaskRepository
from util.datetime import jst_today

logger = get_logger(__name__)


class FetchTasksUsecase:
    def __init__(self, task_repository: TaskRepository) -> None:
        self.task_repository = task_repository

    def execute(self, status_list: list[str], start_date: date | None = None) -> list[Task]:
        return self.task_repository.search(
            status_list=status_list,
            start_datetime=start_date,
            start_datetime_end=start_date,
        )

    def current(self) -> list[Task]:
        return self.execute(status_list=["ToDo", "InProgress"], start_date=jst_today())
