from custom_logger import get_logger
from task.domain.task import Task
from task.domain.task_repository import TaskRepository
from task.domain.task_status import TaskStatusType

logger = get_logger(__name__)


class FindLatestInprogressTaskUsecase:
    def __init__(self, task_repository: TaskRepository) -> None:
        self._task_repository = task_repository

    def execute(self) -> Task | None:
        tasks = self._task_repository.search(status_list=[TaskStatusType.IN_PROGRESS])
        print(tasks)
        return tasks[0]
