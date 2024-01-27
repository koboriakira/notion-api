import os
from notion_client_wrapper.client_wrapper import ClientWrapper, BasePage
from custom_logger import get_logger

logger = get_logger(__name__)

class FindTaskUsecase:
    def __init__(self):
        self.client = ClientWrapper(notion_secret=os.getenv("NOTION_SECRET"))

    def execute(self,
                id: str,
                ) -> dict:
        page = self.client.retrieve_page(page_id=id)
        return self._convert_task(page)

    def _convert_task(self, task: BasePage) -> dict:
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
