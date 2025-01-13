from lotion import Lotion
from lotion.block.rich_text import RichText, RichTextBuilder

from custom_logger import get_logger
from notion_databases.project import Project
from notion_databases.project_prop.project_status import ProjectStatusType
from project.project_repository import ProjectRepository
from task.task_factory import TaskFactory
from task.task_repository import TaskRepository

logger = get_logger(__name__)


def _generate_title_rich_text(title: str | None, relation_page_id: str | None) -> RichText:
    if title is not None:
        return RichTextBuilder.create().add_text(title).build()
    if relation_page_id is not None:
        return RichTextBuilder.create().add_page_mention(relation_page_id).build()
    raise ValueError("title or relation_page_id must be specified")


class CreateProjectService:
    def __init__(self, task_repository: TaskRepository, project_repository: ProjectRepository) -> None:
        self._lotion = Lotion.get_instance()
        self._task_repository = task_repository
        self._project_repository = project_repository

    def execute(
        self,
        project_name: str | None = None,
        relation_page_id: str | None = None,
        tasks_request: list[dict[str, RichText]] | None = None,
    ) -> Project:
        tasks_request = tasks_request or []

        project = self._lotion.create_page(
            Project.generate(
                title=_generate_title_rich_text(project_name, relation_page_id),
                project_status=ProjectStatusType.IN_PROGRESS,
            ),
        )
        for task_req in tasks_request:
            title_rich_text = task_req["title_rich_text"]
            task = TaskFactory.create_todo_task(
                title=title_rich_text,
                project_id=project.id,
            )
            self._lotion.create_page(task)
        return project
