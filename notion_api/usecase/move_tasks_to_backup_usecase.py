from datetime import datetime, timedelta

from custom_logger import get_logger
from domain.task.task_repository import TaskRepository
from domain.task.task_status import TaskStatusType
from util.datetime import jst_now

logger = get_logger(__name__)


class MoveTasksToBackupUsecase:
    MIN_DATETIME = datetime(1970, 1, 1)

    def __init__(self, task_repository: TaskRepository) -> None:
        self.task_repository = task_repository

    def execute(self) -> None:
        # まず全てのタスクを集める
        tasks = self.task_repository.search(status_list=[TaskStatusType.DONE])

        # 直近更新されたものは無視
        target_datetime = jst_now() - timedelta(days=14)
        tasks_moving_to_backup = [t for t in tasks if t.last_edited_time.is_between(self.MIN_DATETIME, target_datetime)]

        # バックアップ用のデータベースに移動
        for task in tasks_moving_to_backup:
            self.task_repository.move_to_backup(task)
            print(task.get_title().text + "をバックアップに移動しました。")


if __name__ == "__main__":
    # python -m notion_api.usecase.move_tasks_to_backup_usecase
    from task.infrastructure.task_repository_impl import TaskRepositoryImpl

    usecase = MoveTasksToBackupUsecase(
        task_repository=TaskRepositoryImpl(),
    )
    usecase.execute()
