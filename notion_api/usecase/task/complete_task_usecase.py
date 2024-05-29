from task.domain.task import Task
from task.domain.task_repository import TaskRepository
from task.domain.task_status import TaskStatusType


class CompleteTaskUsecase:
    def __init__(self, task_repository: TaskRepository) -> None:
        self._task_repository = task_repository

    def execute(self, task_id: str) -> Task:
        task = self._task_repository.find_by_id(task_id=task_id)
        if task is not None:
            task.update_status(TaskStatusType.DONE)
        return self._task_repository.save(task)
