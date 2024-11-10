from notion_client_wrapper.page.page_id import PageId
from task.domain.task import ToDoTask
from task.domain.task_repository import TaskRepository
from task.domain.task_status import TaskStatusType
from custom_logger import get_logger


class StartTaskUsecase:
    def __init__(self, task_repository: TaskRepository) -> None:
        self._task_repository = task_repository
        self._logger = get_logger(__name__)

    def execute(self, page_id: PageId | None = None) -> ToDoTask:
        """
        Start the task.
        If the task page is not specified, search "IsStarted" property in the database and start the task.
        """
        if page_id is None:
            tasks = self._task_repository.search(is_started=True)
            if len(tasks) == 0:
                self._logger.info("Task not found.")
                raise ValueError("Task not found.")

            self._logger.info("Start the task. task_length=%s", len(tasks))
            to_do_tasks = [self.execute(task.page_id) for task in tasks if task.is_started]
            return to_do_tasks[0]

        task = self._task_repository.find_by_id(task_id=page_id.value)
        if task is None:
            msg = f"Task not found. page_id={page_id.value}"
            raise ValueError(msg)
        task = task.update_status(TaskStatusType.IN_PROGRESS).update_pomodoro_count(number=task.pomodoro_count + 1).update_is_started(False)
        return self._task_repository.save(task)

if __name__ == "__main__":
    # python -m notion_api.usecase.task.start_task_usecase
    from task.infrastructure.task_repository_impl import TaskRepositoryImpl
    task_repository = TaskRepositoryImpl()
    usecase = StartTaskUsecase(task_repository=task_repository)
    usecase.execute()
