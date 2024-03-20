from custom_logger import get_logger
from domain.task.task_repository import TaskRepository
from usecase.service.base_page_converter import BasePageConverter

logger = get_logger(__name__)

class FindTaskUsecase:
    def __init__(self, task_repository: TaskRepository) -> None:
        self._task_repository = task_repository


    def execute(self, task_id: str) -> dict:
        task = self._task_repository.find_by_id(task_id=task_id)
        return BasePageConverter.to_task(page=task)
