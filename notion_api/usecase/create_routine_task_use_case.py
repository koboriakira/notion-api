from datetime import datetime

from task.domain.routine_repository import RoutineRepository
from task.domain.task_kind import TaskKindType
from task.domain.task_repository import TaskRepository
from task.domain.task_status import TaskStatusType
from task.task_factory import TaskFactory
from util.datetime import JST


class CreateRoutineTaskUseCase:
    def __init__(self, task_repository: TaskRepository, routine_repository: RoutineRepository) -> None:
        self.task_repository = task_repository
        self.routine_repository = routine_repository

    def execute(self) -> None:
        routine_tasks = self.routine_repository.fetch_all()
        next_tasks = self.task_repository.search(
            status_list=[TaskStatusType.TODO, TaskStatusType.IN_PROGRESS],
            kind_type_list=[TaskKindType.SCHEDULE, TaskKindType.NEXT_ACTION],
        )
        next_task_titles = [task.get_title().text for task in next_tasks]

        for routine_task in routine_tasks:
            title = routine_task.get_title_text()
            if title in next_task_titles:
                print(f"Routine task {title} is already exists.")
                continue
            next_date = routine_task.get_next_date()
            start_date = datetime.combine(next_date, datetime.min.time(), JST)
            due_date = datetime.combine(next_date, routine_task.due_time(), JST) if routine_task.due_time() else None
            task_kind_type = TaskKindType.NEXT_ACTION
            task = TaskFactory.create_todo_task(
                title=title,
                task_kind_type=task_kind_type,
                start_date=start_date,
                due_date=due_date,
                blocks=routine_task.block_children,
            )
            print(f"Create task: {task.get_title_text()}")
            self.task_repository.save(task=task)


if __name__ == "__main__":
    # python -m notion_api.usecase.create_routine_task_use_case
    from task.infrastructure.routine_repository_impl import RoutineRepositoryImpl
    from task.infrastructure.task_repository_impl import TaskRepositoryImpl

    task_repository = TaskRepositoryImpl()
    routine_repository = RoutineRepositoryImpl()
    usecase = CreateRoutineTaskUseCase(task_repository=task_repository, routine_repository=routine_repository)
    usecase.execute()
