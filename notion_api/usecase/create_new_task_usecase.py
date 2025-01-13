from datetime import date, datetime

from lotion import Lotion
from lotion.block.rich_text import RichText, RichTextBuilder

from notion_databases.task_prop.task_kind import TaskKindType
from notion_databases.task_prop.task_status import TaskStatusType
from task.task_factory import TaskFactory
from task.task_repository import TaskRepository


def _generate_title_rich_text(title: str | None, mentioned_page_id: str | None) -> RichText:
    if title is None and mentioned_page_id is None:
        msg = "title と mentioned_page_id のどちらかは必須です"
        raise ValueError(msg)
    rich_text_builder = RichTextBuilder.create()
    if mentioned_page_id is None:
        text = title if title is not None else ""
        return rich_text_builder.add_text(text).build()
    return rich_text_builder.add_page_mention(mentioned_page_id).build()


class CreateNewTaskUsecase:
    def __init__(self, task_repository: TaskRepository) -> None:
        self.task_repository = task_repository
        self._lotion = Lotion.get_instance()

    def execute(  # noqa: PLR0913
        self,
        title: str | None,
        mentioned_page_id: str | None = None,
        start_date: date | datetime | None = None,
        end_date: date | datetime | None = None,
        status: str | None = None,
        task_kind: str | None = None,
    ) -> dict:
        task_kind_type = TaskKindType(task_kind) if task_kind is not None else None
        task_status_type = TaskStatusType(status) if status is not None else None
        task = TaskFactory.create_todo_task(
            title=_generate_title_rich_text(title, mentioned_page_id),
            task_kind_type=task_kind_type,
            start_date=start_date,
            end_date=end_date,
            status=task_status_type,
        )
        task = self._lotion.create_page(task)
        return {
            "id": task.id,
            "url": task.url,
        }


if __name__ == "__main__":
    # python -m notion_api.usecase.create_new_task_usecase
    from task.task_repository_impl import TaskRepositoryImpl

    task_repository = TaskRepositoryImpl()
    usecase = CreateNewTaskUsecase(task_repository=task_repository)
    result = usecase.execute(title="Inbox")
    print(result)
