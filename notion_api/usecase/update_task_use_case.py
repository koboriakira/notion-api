from task.domain.task import Task
from task.domain.task_repository import TaskRepository


class UpdateTaskUsecase:
    def __init__(self, task_repository: TaskRepository) -> None:
        self._task_repository = task_repository

    def execute(self, task_id: str, status: str | None = None) -> Task:
        task = self._task_repository.find_by_id(task_id=task_id)
        if status is not None:
            task = task.update_status(status)
        return self._task_repository.save(task)
