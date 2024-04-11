from datetime import date, datetime, timedelta

from custom_logger import get_logger
from task.domain.task import Task
from task.domain.task_repository import TaskRepository
from task.domain.task_status import TaskStatusType
from util.datetime import jst_today

logger = get_logger(__name__)


class PostponeTaskToNextDayUsecase:
    MIN_DATETIME = datetime.min

    def __init__(self, task_repository: TaskRepository) -> None:
        self._task_repository = task_repository

    def execute(self, target_date: date | None = None) -> list[dict]:
        target_date = target_date or jst_today()

        # 指定日より前の未了タスクを集めて、実施日を指定日に更新
        tasks: list[Task] = self._fetch_past_undone_tasks(target_date)
        self._update_start_datetime(tasks, target_date)

    def _fetch_past_undone_tasks(self, target_date: date) -> list[Task]:
        return self._task_repository.search(
            status_list=[TaskStatusType.TODO, TaskStatusType.IN_PROGRESS],
            start_datetime=self.MIN_DATETIME,
            start_datetime_end=target_date - timedelta(days=1),
        )

    def _update_start_datetime(self, tasks: list[Task], target_date: date) -> Task:
        for task in tasks:
            task.update_start_datetime(target_date)
            self._task_repository.save(task)


if __name__ == "__main__":
    # python -m notion_api.usecase.postpone_task_to_next_day_usecase
    from task.infrastructure.task_repository_impl import TaskRepositoryImpl

    usecase = PostponeTaskToNextDayUsecase(task_repository=TaskRepositoryImpl())
    print(usecase.execute())
