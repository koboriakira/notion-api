import os
from typing import Optional
from datetime import date as DateObject
from datetime import datetime as DatetimeObject
from notion_client_wrapper.client_wrapper import ClientWrapper, BasePage
from domain.database_type import DatabaseType
from domain.task import TaskStatus
from custom_logger import get_logger
from usecase.service.base_page_converter import BasePageConverter

logger = get_logger(__name__)

class FetchTasksUsecase:
    def __init__(self):
        self.client = ClientWrapper(notion_secret=os.getenv("NOTION_SECRET"))

    def execute(self,
                status_list: list[str],
                start_date: Optional[DateObject] = None,
                ) -> list[dict]:
        # まず全てのタスクを集める
        all_pages = self.client.retrieve_database(database_id=DatabaseType.TASK.value)
        all_tasks = [BasePageConverter.to_task(p) for p in all_pages]

        # ステータス条件を取得
        status_cond_list = TaskStatus.get_status_list(status_list)
        status_cond_name_list = [s.value for s in status_cond_list]
        logger.debug(f"status_cond_name_list: {status_cond_name_list}")

        tasks = []
        for task in all_tasks:
            # タスク種別:ゴミ箱は除外する
            if task.get("task_kind") == "ゴミ箱":
                continue

            # 実施日が指定されている場合は、実施日が一致するもののみを返す
            if start_date is not None:
                if task["start_date"] is None:
                    continue
                task_start_date = _convert_to_date(task["start_date"])
                if task_start_date != start_date:
                    continue

            # ステータスが指定されている場合は、ステータスが一致するもののみを返す
            if len(status_cond_list) > 0:
                if task["status"] not in status_cond_name_list:
                    continue
            tasks.append(task)
        return tasks

def _convert_to_date(value: str) -> DateObject:
    if len(value) == 10:
        return DateObject.fromisoformat(value)
    else:
        return DatetimeObject.fromisoformat(value).date()
