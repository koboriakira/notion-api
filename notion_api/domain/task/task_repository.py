from abc import ABCMeta, abstractmethod
from datetime import date, datetime

from domain.task.task import Task
from domain.task.task_kind import TaskKindType
from domain.task.task_status import TaskStatusType


class TaskRepository(metaclass=ABCMeta):
    @abstractmethod
    def search(
        self,
        status_list: list[str | TaskStatusType] | None = None,
        kind_type_list: list[TaskKindType] | None = None,
        start_datetime: date | datetime | None = None,
        start_datetime_end: date | datetime | None = None,
    ) -> list[Task]:
        pass

    @abstractmethod
    def save(self, task: Task) -> Task:
        pass

    @abstractmethod
    def find_by_id(self, task_id: str) -> Task:
        pass

    @abstractmethod
    def move_to_backup(self, task: Task) -> None:
        pass
