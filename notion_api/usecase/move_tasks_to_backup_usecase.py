from datetime import datetime as DatetimeObject
from datetime import timedelta

from custom_logger import get_logger
from domain.database_type import DatabaseType
from domain.task import TaskStatus
from notion_client_wrapper.base_page import BasePage
from notion_client_wrapper.client_wrapper import ClientWrapper
from util.datetime import jst_now

logger = get_logger(__name__)

DATETIME_2000 = DatetimeObject(2000, 1, 1)

class MoveTasksToBackupUsecase:
    def __init__(self):
        self.client = ClientWrapper.get_instance()

    def execute(self) -> None:
        datetime = jst_now() - timedelta(days=14)

        # まず全てのタスクを集める
        all_pages = self.client.retrieve_database(database_id=DatabaseType.TASK.value)
        tasks: list[BasePage] = []
        for page in all_pages:
            # 未了のタスクは無視
            if page.get_status("ステータス").status_name != TaskStatus.DONE.value:
                continue
            # 直近更新されたものは無視
            if not page.last_edited_time.is_between(DATETIME_2000, datetime):
                continue
            tasks.append(page)

        # バックアップ用のデータベースに移動
        for task in tasks:
            print(task.get_title().text)
            properties = [
                task.get_title(),
                task.get_status("ステータス"),
            ]
            if task.get_date("実施日").start is not None:
                properties.append(task.get_date("実施日"))
            if task.get_select("タスク種別") is not None:
                properties.append(task.get_select("タスク種別"))

            # バックアップ用のデータベースにレコードを作成
            self.client.create_page_in_database(
                database_id=DatabaseType.TASK_BK.value,
                properties=properties)

            # タスクを削除
            self.client.remove_page(page_id=task.id)



if __name__ == "__main__":
    # python -m usecase.move_tasks_to_backup_usecase
    usecase = MoveTasksToBackupUsecase()
    usecase.execute()
