from custom_logger import get_logger
from notion_databases.task import Task
from notion_databases.task_prop.task_status import TaskStatusType
from task.domain.task_repository import TaskRepository

logger = get_logger(__name__)


class FindLatestInprogressTaskUsecase:
    def __init__(self, task_repository: TaskRepository) -> None:
        self._task_repository = task_repository

    def execute(self) -> Task | None:
        tasks = self._task_repository.search(
            status_list=[TaskStatusType.IN_PROGRESS],
        )
        if len(tasks) == 0:
            return None

        task_id = tasks[0].id
        return self._task_repository.find_by_id(task_id)
