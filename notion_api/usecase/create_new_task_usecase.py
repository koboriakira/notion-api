from datetime import date, datetime

from lotion.properties import Title

from notion_databases.task_prop.task_kind import TaskKindType
from notion_databases.task_prop.task_status import TaskStatusType
from task.task_repository import TaskRepository
from task.task_factory import TaskFactory


class CreateNewTaskUsecase:
    def __init__(self, task_repository: TaskRepository) -> None:
        self.task_repository = task_repository

    def execute(  # noqa: PLR0913
        self,
        title: str | None,
        mentioned_page_id: str | None = None,
        start_date: date | datetime | None = None,
        end_date: date | datetime | None = None,
        status: str | None = None,
        task_kind: str | None = None,
    ) -> dict:
        title_property = self._generate_title(title=title, mentioned_page_id=mentioned_page_id)
        task_kind_type = TaskKindType(task_kind) if task_kind is not None else None
        task_status_type = TaskStatusType(status) if status is not None else None
        task = TaskFactory.create_todo_task(
            title=title_property,
            task_kind_type=task_kind_type,
            start_date=start_date,
            end_date=end_date,
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
            text = title if title is not None else ""
            return Title.from_plain_text(name="名前", text=text)
        return Title.from_mentioned_page_id(name="名前", page_id=mentioned_page_id)


if __name__ == "__main__":
    # python -m notion_api.usecase.create_new_task_usecase
    from task.task_repository_impl import TaskRepositoryImpl

    task_repository = TaskRepositoryImpl()
    usecase = CreateNewTaskUsecase(task_repository=task_repository)
    result = usecase.execute(title="Inbox")
    print(result)
