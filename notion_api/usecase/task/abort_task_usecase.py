from lotion import BasePage

from notion_databases.task_prop.task_status import TaskStatusType
from task.task_repository import TaskRepository
from task.task_factory import TaskFactory
from util.datetime import jst_now


class AbortTaskUsecase:
    def __init__(self, task_repository: TaskRepository) -> None:
        self._task_repository = task_repository

    def execute(self, page_id: str) -> None:
        task = self._task_repository.find_by_id(task_id=page_id)
        if task is None:
            msg = f"Task not found. page_id={page_id}"
            raise ValueError(msg)

        # タスクを中断した場合、その日のタスクをコピーする
        # 開始日は終日にする
        copied_task = (
            TaskFactory.cast(BasePage.create(properties=task.properties.values, blocks=task.block_children))
            .update_start_datetime(start=jst_now().date())
            .update_status(TaskStatusType.TODO)
        )
        self._task_repository.save(copied_task)

        # 元のタスクは完了にする
        task = task.complete()
        self._task_repository.save(task)


if __name__ == "__main__":
    # python -m notion_api.usecase.task.abort_task_usecase
    from task.task_repository_impl import TaskRepositoryImpl

    task_repository = TaskRepositoryImpl()
    usecase = AbortTaskUsecase(task_repository=task_repository)
    page_id = "1666567a3bbf8059a791fda7b6b846ab"
    usecase.execute(page_id=page_id)
