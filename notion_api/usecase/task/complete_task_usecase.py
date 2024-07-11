from notion_client_wrapper.page.page_id import PageId
from task.domain.task import ToDoTask
from task.domain.task_repository import TaskRepository
from task.domain.task_status import TaskStatusType


class CompleteTaskUsecase:
    def __init__(self, task_repository: TaskRepository) -> None:
        self._task_repository = task_repository

    def execute(self, page_id: PageId) -> ToDoTask:
        task = self._task_repository.find_by_id(task_id=page_id.value)
        if task is None:
            msg = f"Task not found. page_id={page_id.value}"
            raise ValueError(msg)
        task = task.update_status(TaskStatusType.DONE)
        return self._task_repository.save(task)
