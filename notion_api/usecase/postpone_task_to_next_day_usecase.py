from datetime import datetime, timedelta

from custom_logger import get_logger
from task.domain.task import ToDoTask
from task.domain.task_repository import TaskRepository
from task.domain.task_status import TaskStatusType
from util.datetime import jst_today

logger = get_logger(__name__)


class PostponeTaskToNextDayUsecase:
    def __init__(self, task_repository: TaskRepository) -> None:
        self._task_repository = task_repository

    def execute(self) -> None:
        # 指定日より前の未了タスクを集めて、do_tomorrowを実行
        tasks: list[ToDoTask] = self._fetch_past_undone_tasks()
        for task in tasks:
            updated_task = task.do_tomorrow()
            self._task_repository.save(updated_task)

    def _fetch_past_undone_tasks(self) -> list[ToDoTask]:
        yesterday = jst_today() - timedelta(days=1)
        return self._task_repository.search(
            status_list=[TaskStatusType.TODO, TaskStatusType.IN_PROGRESS],
            start_datetime=datetime.min,
            start_datetime_end=yesterday,
        )


if __name__ == "__main__":
    # python -m notion_api.usecase.postpone_task_to_next_day_usecase
    from task.infrastructure.task_repository_impl import TaskRepositoryImpl

    usecase = PostponeTaskToNextDayUsecase(task_repository=TaskRepositoryImpl())
    print(usecase.execute())
