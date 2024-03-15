from abc import ABCMeta, abstractmethod
from datetime import date

from domain.task.task import Task


class TaskRepository(metaclass=ABCMeta):
    @abstractmethod
    def search(
            self,
            status_list: list[str]|None=None,
            start_date: date | None = None) -> list[Task]:
        pass
