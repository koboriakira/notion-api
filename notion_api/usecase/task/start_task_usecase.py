from notion_client_wrapper.page.page_id import PageId
from task.domain.task import Task
from task.domain.task_repository import TaskRepository
from task.domain.task_status import TaskStatusType


class StartTaskUsecase:
    def __init__(self, task_repository: TaskRepository) -> None:
        self._task_repository = task_repository

    def execute(self, page_id: PageId) -> Task:
        task = self._task_repository.find_by_id(task_id=page_id.value)
        if task is None:
            msg = f"Task not found. page_id={page_id.value}"
            raise ValueError(msg)
        task = task.update_status(TaskStatusType.IN_PROGRESS).update_pomodoro_count(number=task.pomodoro_count + 1)
        return self._task_repository.save(task)
