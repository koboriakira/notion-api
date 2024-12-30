from custom_logger import get_logger
from notion_databases.task import Task
from task.domain.task_repository import TaskRepository


class StartTaskUsecase:
    def __init__(self, task_repository: TaskRepository) -> None:
        self._task_repository = task_repository
        self._logger = get_logger(__name__)

    def execute(self, page_id: str) -> Task:
        """
        Start the task.
        """
        task = self._task_repository.find_by_id(task_id=page_id)
        if task is None:
            msg = f"Task not found. page_id={page_id}"
            raise ValueError(msg)
        return self._task_repository.save(task.start())


if __name__ == "__main__":
    # python -m notion_api.usecase.task.start_task_usecase
    from task.infrastructure.task_repository_impl import TaskRepositoryImpl

    task_repository = TaskRepositoryImpl()
    usecase = StartTaskUsecase(task_repository=task_repository)
    # usecase.execute()
