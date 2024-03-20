

from domain.task.task_kind import TaskKindType
from domain.task.task_repository import TaskRepository
from infrastructure.task.routine_repository_impl import RoutineRepositoryImpl
from notion_api.domain.task.task import Task
from util.datetime import jst_today

TODAY = jst_today()
from datetime import datetime


class CreateRoutineTaskUseCase:
    def __init__(
            self,
            task_repository: TaskRepository,
            routine_repository: RoutineRepositoryImpl) -> None:
        self.task_repository = task_repository
        self.routine_repository = routine_repository

    def execute(self) -> None:
        routine_tasks = self.routine_repository.fetch_all()
        next_tasks = self.task_repository.search(task_kind=TaskKindType.NEXT_ACTION)
        next_task_titles = [task.get_title().text for task in next_tasks]

        for routine_task in routine_tasks:
            if routine_task.title in next_task_titles:
                print(f"Routine task {routine_task.title} is already exists.")
                continue
            next_date = routine_task.get_next_date()
            if next_date == TODAY:
                task = Task.create(
                    title=routine_task.title,
                    task_kind_type=TaskKindType.NEXT_ACTION,
                    start_date=datetime(TODAY.year, TODAY.month, TODAY.day),
                )
                self.task_repository.save(task=task)
                continue
            print(f"Create next date: {routine_task.title} {next_date}")

if __name__ == "__main__":
    # python -m notion_api.usecase.create_routine_task_use_case
    from infrastructure.task.task_repository_impl import TaskRepositoryImpl
    task_repository = TaskRepositoryImpl()
    routine_repository = RoutineRepositoryImpl()
    usecase = CreateRoutineTaskUseCase(
        task_repository=task_repository,
        routine_repository=routine_repository)
    usecase.execute()
