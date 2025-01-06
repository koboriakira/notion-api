from datetime import timedelta
from logging import Logger

from lotion import Lotion
from lotion.filter import Builder, Cond

from custom_logger import get_logger
from notion_databases.task import Task, TaskKind, TaskStatus
from notion_databases.task_prop.task_kind import TaskKindType
from notion_databases.task_prop.task_start_date import TaskStartDate
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
        filter_builder = Builder.create()
        status_prop = TaskStatus.from_status_type(TaskStatusType.TODO)
        filter_builder = filter_builder.add(status_prop, Cond.EQUALS)
        kind_prop = TaskKind.from_name(TaskKindType.SCHEDULE.value)
        filter_builder = filter_builder.add(kind_prop, Cond.EQUALS)
        start = TaskStartDate.from_start_date(now)
        filter_builder = filter_builder.add(start, Cond.ON_OR_AFTER)
        end = TaskStartDate.from_start_date(now + timedelta(minutes=3))
        filter_builder = filter_builder.add(end, Cond.ON_OR_BEFORE)
        filter_param = filter_builder.build()

        tasks = self._lotion.retrieve_pages(Task, filter_param)
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
    # usecase._execute_last_edited()
    usecase._execute_scheduled()
