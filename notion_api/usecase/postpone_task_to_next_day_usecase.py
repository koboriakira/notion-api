from datetime import date as DateObject
from datetime import timedelta

from custom_logger import get_logger
from domain.task.task import Task
from domain.task.task_repository import TaskRepository
from domain.task.task_status import TaskStatusType
from util.datetime import jst_today

logger = get_logger(__name__)

class PostponeTaskToNextDayUsecase:
    def __init__(self, task_repository: TaskRepository) -> None:
        self._task_repository = task_repository

    def execute(self,
                date: DateObject | None = None) -> list[dict]:
        # 指定日がない場合は前日を指定
        date = date if date is not None else jst_today() - timedelta(days=1)

        # まず未完了のタスクを集める
        tasks: list[Task] = self._task_repository.search(
            status_list=[TaskStatusType.TODO, TaskStatusType.IN_PROGRESS],
        )

        # 実施日が過去のタスクに絞る
        tasks = [task for task in tasks if task.start_date is not None]
        tasks = [task for task in tasks if task.start_date <= date]

        # 実施日を翌日に更新
        tomorrow = date + timedelta(days=1)
        for task in tasks:
            task.update_start_datetime(tomorrow)
            self._task_repository.save(task)

if __name__ == "__main__":
    # python -m notion_api.usecase.postpone_task_to_next_day_usecase
    from infrastructure.task.task_repository_impl import TaskRepositoryImpl
    usecase = PostponeTaskToNextDayUsecase(task_repository=TaskRepositoryImpl())
    print(usecase.execute())
