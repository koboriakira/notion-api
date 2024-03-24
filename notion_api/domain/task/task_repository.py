from abc import ABCMeta, abstractmethod
from datetime import date

from domain.task.task import Task
from domain.task.task_kind import TaskKindType
from domain.task.task_status import TaskStatusType


class TaskRepository(metaclass=ABCMeta):
    @abstractmethod
    def search(
            self,
            status_list: list[str|TaskStatusType]|None=None,
            task_kind: TaskKindType|None=None,
            start_date: date | None = None) -> list[Task]:
        pass

    @abstractmethod
    def save(self, task: Task) -> Task:
        pass

    @abstractmethod
    def find_by_id(self, task_id: str) -> Task:
        pass
