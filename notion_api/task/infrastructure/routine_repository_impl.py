from lotion import Lotion
from lotion.base_page import BasePage

from common.value.database_type import DatabaseType
from task.domain.routine_repository import RoutineRepository
from task.domain.routine_task import RoutineTask


class RoutineRepositoryImpl(RoutineRepository):
    def __init__(self, notion_client_wrapper: Lotion | None = None) -> None:
        self.client = notion_client_wrapper or Lotion.get_instance()

    def fetch_all(self) -> list[RoutineTask]:
        base_pages = self.client.retrieve_database(
            database_id=DatabaseType.TASK_ROUTINE.value,
            include_children=True,
        )
        return [self._cast(base_page) for base_page in base_pages]

    def _cast(self, base_page: BasePage) -> RoutineTask:
        return RoutineTask(
            properties=base_page.properties,
            block_children=base_page.block_children,
            id_=base_page.id_,
            url=base_page.url,
            created_time=base_page.created_time,
            last_edited_time=base_page.last_edited_time,
            created_by=base_page.created_by,
            last_edited_by=base_page.last_edited_by,
            cover=base_page.cover,
            icon=base_page.icon,
            archived=base_page.archived,
            parent=base_page.parent,
        )


if __name__ == "__main__":
    # python -m notion_api.infrastructure.task.routine_repository_impl
    repository = RoutineRepositoryImpl()
    tasks = repository.fetch_all()
    for task in tasks:
        print(task)
