from datetime import date as DateObject

from custom_logger import get_logger
from task.domain.task import Task
from task.infrastructure.task_repository_impl import TaskRepositoryImpl
from usecase.fetch_tasks_usecase import FetchTasksUsecase
from usecase.postpone_task_to_next_day_usecase import PostponeTaskToNextDayUsecase

logger = get_logger(__name__)


def fetch_tasks(start_date: DateObject | None = None, status_list: list[str] | None = None) -> list[Task]:
    """タスク一覧を取得"""
    status_list = status_list or []
    logger.debug(f"start_date: {start_date}")
    logger.debug(f"status_list: {status_list}")
    usecase = FetchTasksUsecase(task_repository=TaskRepositoryImpl())
    return usecase.execute(status_list=status_list, start_date=start_date)


def get_current_tasks() -> list[Task]:
    """今日のタスクを取得"""
    usecase = FetchTasksUsecase(task_repository=TaskRepositoryImpl())
    return usecase.current()


def postpone_to_next_day(date: DateObject | None = None) -> list[Task]:
    """実施日を翌日に延期"""
    logger.debug(f"date: {date}")
    usecase = PostponeTaskToNextDayUsecase(task_repository=TaskRepositoryImpl())
    return usecase.execute(target_date=date)
