from abc import ABCMeta, abstractmethod
from datetime import date

from domain.task.task import Task
from domain.task.task_kind import TaskKindType


class TaskRepository(metaclass=ABCMeta):
    @abstractmethod
    def search(
            self,
            status_list: list[str]|None=None,
            task_kind: TaskKindType|None=None,
            start_date: date | None = None) -> list[Task]:
        pass
