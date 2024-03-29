from datetime import date, datetime

from domain.task.task import Task
from domain.task.task_kind import TaskKindType
from domain.task.task_repository import TaskRepository
from domain.task.task_status import TaskStatusType
from notion_client_wrapper.properties import Title


class CreateNewTaskUsecase:
    def __init__(self, task_repository: TaskRepository) -> None:
        self.task_repository = task_repository

    def execute(  # noqa: PLR0913
            self,
            title: str | None,
            mentioned_page_id: str | None,
            start_date: date | datetime | None = None,
            status: str | None = None,
            task_kind: str | None = None) -> dict:
        title_property = self._generate_title(title=title, mentioned_page_id=mentioned_page_id)
        task_kind_type = TaskKindType.from_text(task_kind) if task_kind is not None else None
        task_status_type = TaskStatusType.from_text(status) if status is not None else None
        task = Task.create(
            title=title_property,
            task_kind_type=task_kind_type,
            start_date=start_date,
            status=task_status_type,
        )
        task = self.task_repository.save(task)
        return {
            "id": task.id,
            "url": task.url,
        }

    def _generate_title(self, title: str | None, mentioned_page_id: str | None) -> Title:
        if title is None and mentioned_page_id is None:
            msg = "title と mentioned_page_id のどちらかは必須です"
            raise ValueError(msg)
        if mentioned_page_id is None:
            return Title.from_plain_text(name="名前", text=title)
        if mentioned_page_id is not None:
            return Title.from_mentioned_page_id(name="名前", page_id=mentioned_page_id)
        raise NotImplementedError
