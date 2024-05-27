from common.value.database_type import DatabaseType
from notion_client_wrapper.client_wrapper import ClientWrapper
from task.domain.routine_repository import RoutineRepository
from task.domain.routine_task import RoutineTask


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
