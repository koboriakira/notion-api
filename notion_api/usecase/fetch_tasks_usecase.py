import os
from typing import Optional
from datetime import date as DateObject
from notion_client_wrapper.client_wrapper import ClientWrapper, BasePage
from domain.database_type import DatabaseType
from domain.task import TaskStatus
from custom_logger import get_logger

logger = get_logger(__name__)

class FetchTasksUsecase:
    def __init__(self):
        self.client = ClientWrapper(notion_secret=os.getenv("NOTION_SECRET"))

    def execute(self,
                status_list: list[str],
                start_date: Optional[DateObject] = None,
                ) -> list[dict]:
        # まず全てのタスクを集める
        all_tasks = self.client.retrieve_database(database_id=DatabaseType.TASK.value)
        all_tasks = [self._convert_project(task) for task in all_tasks]

        # ステータス条件を取得
        status_cond_list = TaskStatus.get_status_list(status_list)
        status_cond_name_list = [s.value for s in status_cond_list]
        logger.debug(f"status_cond_name_list: {status_cond_name_list}")

        tasks = []
        for task in all_tasks:
            # 実施日が指定されている場合は、実施日が一致するもののみを返す
            if start_date is not None and task["start_date"] is not None:
                if DateObject.fromisoformat(task["start_date"]) != start_date:
                    continue

            # ステータスが指定されている場合は、ステータスが一致するもののみを返す
            if len(status_cond_list) > 0:
                if task["status"] not in status_cond_name_list:
                    continue
            tasks.append(task)

        return tasks

    def _convert_project(self, task: BasePage) -> dict:
        status = task.get_status(name="ステータス")
        start_date = task.get_date(name="実施日")
        task_kind = task.get_select(name="タスク種別")
        return {
            "id": task.id,
            "url": task.url,
            "title": task.get_title().text,
            "created_at": task.created_time.value,
            "updated_at": task.last_edited_time.value,
            "status": status.status_name,
            "task_kind": task_kind.name if task_kind is not None else None,
            "start_date": start_date.start if start_date is not None else None,
        }
