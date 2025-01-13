from dataclasses import dataclass

from lotion import Lotion
from lotion.block.rich_text import RichText, RichTextBuilder

from custom_logger import get_logger
from notion_databases.project import Project
from notion_databases.project_prop.project_status import ProjectStatusType
from task.task_factory import TaskFactory

logger = get_logger(__name__)


def _generate_title_rich_text(title: str | None, relation_page_id: str | None) -> RichText:
    if title is not None:
        return RichTextBuilder.create().add_text(title).build()
    if relation_page_id is not None:
        return RichTextBuilder.create().add_page_mention(relation_page_id).build()
    raise ValueError("title or relation_page_id must be specified")


@dataclass
class TaskRequestTitle:
    value: str | RichText


@dataclass
class TaskRequest:
    title: TaskRequestTitle


class CreateProjectService:
    def __init__(self, lotion: Lotion | None = None) -> None:
        self._lotion = lotion or Lotion.get_instance()

    def execute(
        self,
        project_name: str | None = None,
        relation_page_id: str | None = None,
        tasks_request: list[TaskRequest] | None = None,
    ) -> Project:
        project = self._lotion.create_page(
            Project.generate(
                title=_generate_title_rich_text(project_name, relation_page_id),
                project_status=ProjectStatusType.IN_PROGRESS,
            ),
        )
        if tasks_request is None:
            task = TaskFactory.create_todo_task(
                title="タスクを検討する",
                project_id=project.id,
            )
            return project

        for task_req in tasks_request:
            title = task_req.title.value
            task = TaskFactory.create_todo_task(
                title=title,
                project_id=project.id,
            )
            self._lotion.create_page(task)
        return project


if __name__ == "__main__":
    # python -m notion_api.usecase.project.create_project_service
    service = CreateProjectService()
    service.execute(
        relation_page_id="f8d8a1263a9c468ca9be1bdd9954a9a3",
    )
