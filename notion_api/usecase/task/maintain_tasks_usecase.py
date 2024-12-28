from datetime import datetime, timedelta
from logging import Logger

from custom_logger import get_logger
from task.domain.task_repository import TaskRepository
from util.datetime import jst_now
from util.line.line_client import LineClient


class MaintainTasksUsecase:
    def __init__(self, task_repository: TaskRepository, logger: Logger | None = None) -> None:
        self._task_repository = task_repository
        self._logger = logger or get_logger(__name__)
        self._line_client = LineClient.get_instance()

    def execute(self, last_edited_at: datetime) -> None:
        tasks = self._task_repository.search(last_edited_at=last_edited_at)

        for task in tasks:
            if task.status.is_todo() and task.is_scheduled():
                self._logger.info(f"「予定」タスクを処理: {task.get_title_text()}")
                self._task_repository.save(task=task.start())
                self._line_client.push_message(f"タスク「{task.get_title_text()}」を開始しました")
            if task.is_completed and not task.get_title_text().startswith("✔️"):
                self._logger.info(f"チェックマークをつける: {task.get_title_text()}")
                self._task_repository.save(task=task.add_check_prefix())


if __name__ == "__main__":
    # python -m notion_api.usecase.task.maintain_tasks_usecase
    from task.infrastructure.task_repository_impl import TaskRepositoryImpl

    task_repository = TaskRepositoryImpl()
    usecase = MaintainTasksUsecase(task_repository=task_repository)
    last_edited_at = jst_now() - timedelta(minutes=30)
    usecase.execute(last_edited_at=last_edited_at)
