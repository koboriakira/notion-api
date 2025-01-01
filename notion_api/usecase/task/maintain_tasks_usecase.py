from datetime import timedelta
from logging import Logger

from lotion import Lotion

from custom_logger import get_logger
from notion_databases.task import Task, TaskStartDate, TaskStatus
from notion_databases.task_prop.task_status import TaskStatusType
from util.datetime import jst_now
from util.line.line_client import LineClient


class MaintainTasksUsecase:
    def __init__(self, logger: Logger | None = None) -> None:
        self._logger = logger or get_logger(__name__)
        self._line_client = LineClient.get_instance()
        self._lotion = Lotion.get_instance(logger=self._logger)

    def execute(self) -> None:
        self._execute_scheduled()
        self._execute_last_edited()

    def _execute_scheduled(self) -> None:
        now = jst_now()
        start_prop = TaskStartDate.from_range(now)
        end_prop = TaskStartDate.from_range(now + timedelta(minutes=3))
        status_prop = TaskStatus.from_status_type(TaskStatusType.TODO)
        tasks = self._lotion.search_pages(Task, [start_prop, end_prop, status_prop])
        for task in tasks:
            self._lotion.update(task.start())
            self._line_client.push_message(f"タスク「{task.get_title_text()}」を開始しました")

    def _execute_last_edited(self) -> None:
        latest_edited_at = jst_now() - timedelta(minutes=10)
        tasks = self._lotion.search_page_by_last_edited_at(Task, start=latest_edited_at)

        for task in tasks:
            if task.is_completed and not task.get_title_text().startswith("✔️"):
                self._logger.info(f"チェックマークをつける: {task.get_title_text()}")
                self._lotion.update(task.add_check_prefix())


if __name__ == "__main__":
    # python -m notion_api.usecase.task.maintain_tasks_usecase

    usecase = MaintainTasksUsecase()
    usecase._execute_last_edited()
