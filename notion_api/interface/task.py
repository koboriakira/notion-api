from typing import Optional
from datetime import date as DateObject
from custom_logger import get_logger
from usecase.fetch_tasks_usecase import FetchTasksUsecase

logger = get_logger(__name__)

def fetch_tasks(start_date: Optional[DateObject] = None,
                status_list: list[str] = []) -> list[dict]:
    """ タスク一覧を取得 """
    logger.debug(f"start_date: {start_date}")
    logger.debug(f"status_list: {status_list}")
    usecase = FetchTasksUsecase()
    return usecase.execute(status_list=status_list,
                           start_date=start_date
                           )
