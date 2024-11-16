from abc import ABCMeta, abstractmethod
from datetime import date, datetime

from notion_client_wrapper.page.page_id import PageId
from task.domain.task import Task
from task.domain.task_kind import TaskKindType
from task.domain.task_status import TaskStatusType


class TaskRepository(metaclass=ABCMeta):
    @abstractmethod
    def search(  # noqa: PLR0913
        self,
        status_list: list[str | TaskStatusType] | None = None,
        kind_type_list: list[TaskKindType] | None = None,
        start_datetime: date | datetime | None = None,
        start_datetime_end: date | datetime | None = None,
        project_id: PageId | None = None,
        do_tomorrow_flag: bool | None = None,
        is_started: bool | None = None,
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
