from task.domain.task import ToDoTask
from task.domain.task_repository import TaskRepository


class UpdateTaskUsecase:
    def __init__(self, task_repository: TaskRepository) -> None:
        self._task_repository = task_repository

    def execute(self, task_id: str, pomodoro_count: int, status: str | None = None) -> ToDoTask:
        task = self._task_repository.find_by_id(task_id=task_id)
        task = task.update_status(status).update_pomodoro_count(pomodoro_count)
        return self._task_repository.save(task)
