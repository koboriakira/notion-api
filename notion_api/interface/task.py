from datetime import date as DateObject

from custom_logger import get_logger
from usecase.fetch_tasks_usecase import FetchTasksUsecase
from usecase.find_task_usecase import FindTaskUsecase
from usecase.postpone_task_to_next_day_usecase import PostponeTaskToNextDayUsecase

logger = get_logger(__name__)

def fetch_tasks(start_date: DateObject | None = None,
                status_list: list[str] = []) -> list[dict]:
    """ タスク一覧を取得 """
    logger.debug(f"start_date: {start_date}")
    logger.debug(f"status_list: {status_list}")
    usecase = FetchTasksUsecase()
    return usecase.execute(status_list=status_list,
                           start_date=start_date,
                           )

def get_current_tasks() -> list[dict]:
    """ 今日のタスクを取得 """
    usecase = FetchTasksUsecase()
    return usecase.current()

def find_task(id: str) -> dict:
    """ タスクを取得 """
    usecase = FindTaskUsecase()
    return usecase.execute(id=id)


def postpone_to_next_day(date: DateObject | None = None) -> list[dict]:
    """ 実施日を翌日に延期 """
    logger.debug(f"date: {date}")
    usecase = PostponeTaskToNextDayUsecase()
    return usecase.execute(date=date)
