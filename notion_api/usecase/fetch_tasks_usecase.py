from datetime import date

from custom_logger import get_logger
from domain.task.task_repository import TaskRepository
from usecase.service.base_page_converter import BasePageConverter
from util.datetime import jst_today

logger = get_logger(__name__)

class FetchTasksUsecase:
    def __init__(self, task_repository: TaskRepository) -> None:
        self.task_repository = task_repository or TaskRepositoryImpl()

    def execute(
            self,
            status_list: list[str],
            start_date: date | None = None) -> list[dict]:
        tasks = self.task_repository.search(status_list=status_list, start_date=start_date)
        # FIXME: このままTaskを返すようにリファクタリングする
        return [BasePageConverter.to_task(t) for t in tasks]

    def current(self) -> list[dict]:
        return self.execute(status_list=["ToDo", "InProgress"], start_date=jst_today())
