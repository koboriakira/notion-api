from datetime import datetime, timedelta
from logging import Logger

from custom_logger import get_logger
from task.domain.task_repository import TaskRepository
from task.domain.task_status import TaskStatusType
from task.task_factory import TaskFactory
from util.datetime import jst_now


class MaintainTasksUsecase:
    def __init__(self, task_repository: TaskRepository, logger: Logger | None = None) -> None:
        self._task_repository = task_repository
        self._logger = logger or get_logger(__name__)

    def execute(self, last_edited_at: datetime) -> None:
        tasks = self._task_repository.search(last_edited_at=last_edited_at)

        for task in tasks:
            if task.is_do_tomorrow:
                self._logger.info(f"「明日やる」タスクを処理: {task.title}")
                self._task_repository.save(task=task.do_tomorrow())
            # if len(task.project_id_list) > 0 and task.kind is None:
            #     self._logger.info(f"タスク種別のないプロジェクト関連タスクを処理: {task.title}")
            #     self._task_repository.save(task=task.update_kind(TaskKindType.NEXT_ACTION))
            if task.is_completed_flag:
                self._logger.info(f"「_完了チェック」タスクを処理: {task.title}")
                self._task_repository.save(task=task.complete())
            if task.is_started:
                self._logger.info(f"「_開始チェック」タスクを処理: {task.title}")
                self._task_repository.save(task=task.start())
            if task.is_later_flag and not task.status.is_done():
                self._logger.info(f"「_あとでチェック」タスクを処理: {task.title}")
                # このタスクは完了にして、新規TODOタスクを作成
                self._task_repository.save(task=task.complete())
                new_task = TaskFactory.create_todo_task(
                    title=task.title,
                    task_kind_type=task.kind,
                    start_date=jst_now().date(),
                    status=TaskStatusType.TODO,
                    blocks=task.block_children,
                )
                self._task_repository.save(task=new_task)


if __name__ == "__main__":
    # python -m notion_api.usecase.task.maintain_tasks_usecase
    from task.infrastructure.task_repository_impl import TaskRepositoryImpl

    task_repository = TaskRepositoryImpl()
    usecase = MaintainTasksUsecase(task_repository=task_repository)
    last_edited_at = jst_now() - timedelta(minutes=30)
    usecase.execute(last_edited_at=last_edited_at)
