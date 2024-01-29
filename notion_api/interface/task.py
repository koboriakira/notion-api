from typing import Optional
from datetime import date as DateObject
from custom_logger import get_logger
from usecase.fetch_tasks_usecase import FetchTasksUsecase
from usecase.find_task_usecase import FindTaskUsecase
from usecase.create_new_task_usecase import CreateNewTaskUsecase

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

def find_task(id: str) -> dict:
    """ タスクを取得 """
    usecase = FindTaskUsecase()
    return usecase.execute(id=id)

def create_new_page(title: str, start_date: Optional[DateObject] = None) -> dict:
    """ タスクを作成 """
    usecase = CreateNewTaskUsecase()
    return usecase.handle(title=title, start_date=start_date)