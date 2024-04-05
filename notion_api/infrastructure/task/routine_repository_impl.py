from domain.database_type import DatabaseType
from domain.task.routine_repository import RoutineRepository
from domain.task.routine_task import RoutineTask
from notion_client_wrapper.base_page import BasePage
from notion_client_wrapper.client_wrapper import ClientWrapper


class RoutineConverter:
    @staticmethod
    def convert(page: BasePage) -> RoutineTask:
        title = page.get_title().text
        routine_type = page.get_select("周期")
        if routine_type is None:
            return None
        return RoutineTask.create(title=title, routine_type_text=routine_type.selected_name)


class RoutineRepositoryImpl(RoutineRepository):
    def __init__(self, notion_client_wrapper: ClientWrapper | None = None) -> None:
        self.client = notion_client_wrapper or ClientWrapper.get_instance()

    def fetch_all(self) -> list[RoutineTask]:
        return self.client.retrieve_database(
            database_id=DatabaseType.TASK_ROUTINE.value,
            page_model=RoutineTask,
            include_children=True,
        )


if __name__ == "__main__":
    # python -m notion_api.infrastructure.task.routine_repository_impl
    repository = RoutineRepositoryImpl()
    tasks = repository.fetch_all()
    for task in tasks:
        print(task)
