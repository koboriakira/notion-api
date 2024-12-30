from notion_databases.task import Task
from notion_databases.task_prop.task_status import TaskStatusType
from task.task_repository import TaskRepository


class CompleteTaskUsecase:
    def __init__(self, task_repository: TaskRepository) -> None:
        self._task_repository = task_repository

    def execute(self, page_id: str) -> Task:
        task = self._task_repository.find_by_id(task_id=page_id)
        if task is None:
            msg = f"Task not found. page_id={page_id}"
            raise ValueError(msg)
        task = task.update_status(TaskStatusType.DONE)
        return self._task_repository.save(task)
