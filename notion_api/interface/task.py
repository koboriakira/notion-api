from typing import Optional
from datetime import date as DateObject
from custom_logger import get_logger
from usecase.fetch_tasks_usecase import FetchTasksUsecase

logger = get_logger(__name__)

def fetch_tasks(start_date: Optional[DateObject] = None) -> list[dict]:
    """ タスク一覧を取得 """
    logger.debug(f"start_date: {start_date}")
    usecase = FetchTasksUsecase()
    return usecase.execute(start_date=start_date)
