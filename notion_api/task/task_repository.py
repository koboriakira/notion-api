from abc import ABCMeta, abstractmethod
from datetime import date, datetime

from notion_databases.task import Task
from notion_databases.task_prop.task_kind import TaskKindType
from notion_databases.task_prop.task_status import TaskStatusType


class TaskRepository(metaclass=ABCMeta):
    @abstractmethod
    def search(  # noqa: PLR0913
        self,
        status_list: list[str | TaskStatusType] | None = None,
        kind_type_list: list[TaskKindType] | None = None,
        start_datetime: date | datetime | None = None,
        start_datetime_end: date | datetime | None = None,
        project_id: str | None = None,
        last_edited_at: datetime | None = None,
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

    @abstractmethod
    def delete(self, task: Task) -> None:
        pass
