from datetime import date as DateObject
from datetime import timedelta

from custom_logger import get_logger
from domain.database_type import DatabaseType
from domain.task import TaskStatus
from notion_client_wrapper.client_wrapper import ClientWrapper
from notion_client_wrapper.properties import Date
from usecase.service.base_page_converter import BasePageConverter
from util.datetime import jst_today

logger = get_logger(__name__)

class PostponeTaskToNextDayUsecase:
    def __init__(self):
        self.client = ClientWrapper.get_instance()

    def execute(self,
                date: DateObject | None = None) -> list[dict]:
        # 指定日がない場合は前日を指定
        date = date if date is not None else jst_today() - timedelta(days=1)

        # まず全てのタスクを集める
        all_pages = self.client.retrieve_database(database_id=DatabaseType.TASK.value)

        # 実施日が過去のタスクに絞る
        filtered_tasks = []
        for page in all_pages:
            if page.get_status("ステータス").status_name == TaskStatus.DONE.value:
                continue
            start_date = page.get_date("実施日")
            if start_date.start is None:
                continue
            if DateObject.fromisoformat(start_date.start[:10]) <= date:
                filtered_tasks.append(BasePageConverter.to_task(page))

        # 実施日を翌日に更新
        tomorrow = date + timedelta(days=1)
        for task in filtered_tasks:
            print(f"postpone: {task['url']}")
            page_id = task["id"]
            date_property = Date.from_start_date(name="実施日", start_date=tomorrow)
            self.client.update_page(
                page_id=page_id,
                properties=[date_property],
            )

        return filtered_tasks

if __name__ == "__main__":
    # python -m notion_api.usecase.postpone_task_to_next_day_usecase
    usecase = PostponeTaskToNextDayUsecase()
    print(usecase.execute())
