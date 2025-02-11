from datetime import date, timedelta

from lotion import Lotion

from notion_databases.habit import HabitTracker
from notion_databases.routine_task import RoutineTask
from notion_databases.task import Task
from notion_databases.task_prop.task_kind import TaskKindType
from notion_databases.task_prop.task_status import TaskStatusType
from task.task_factory import TaskFactory
from task.task_repository import TaskRepository
from util.datetime import jst_tommorow


class CreateRoutineTaskUseCase:
    def __init__(self, task_repository: TaskRepository, lotion: Lotion | None = None) -> None:
        self.task_repository = task_repository
        self._lotion = lotion or Lotion.get_instance()

    def execute(self, date_: date) -> None:
        next_tasks = self.task_repository.search(
            status_list=[TaskStatusType.TODO, TaskStatusType.IN_PROGRESS],
            kind_type_list=[TaskKindType.ROUTINE, TaskKindType.HABIT],
            start_datetime=date_,
            start_datetime_end=date_ + timedelta(days=90),
        )
        self._execute_routines(date_, next_tasks)
        # self._execute_habits(date_, next_tasks)

    def _execute_routines(self, date: date, next_tasks: list[Task]) -> None:
        routine_tasks = self._lotion.retrieve_pages(RoutineTask, include_children=True)
        next_tasks = self.task_repository.search(
            status_list=[TaskStatusType.TODO, TaskStatusType.IN_PROGRESS],
            kind_type_list=[TaskKindType.ROUTINE, TaskKindType.HABIT],
            start_datetime=date,
            start_datetime_end=date + timedelta(days=90),
        )
        next_task_titles = [task.get_title().text for task in next_tasks if task.kind.to_enum() == TaskKindType.ROUTINE]

        for routine_task in routine_tasks:
            title = routine_task.get_title_text()
            if title in next_task_titles:
                print(f"Routine task {title} is already exists.")
                continue
            start_date, end_date = routine_task.get_next_schedule(basis_date=date)
            routine_todo_task = TaskFactory.create_todo_task(
                title=title,
                task_kind_type=TaskKindType.ROUTINE,
                start_date=start_date,
                end_date=end_date,
                blocks=routine_task.block_children if routine_task.get_title_text() != "買い物 & 料理" else [],
            )
            print(f"Create task: {routine_todo_task.get_title_text()}")
            self._lotion.create_page(routine_todo_task)

    def _execute_habits(self, date: date, next_tasks: list[Task]) -> None:
        habits = self._lotion.retrieve_pages(HabitTracker, include_children=True)
        next_task_titles = [task.get_title().text for task in next_tasks if task.kind.to_enum() == TaskKindType.HABIT]
        for habit in habits:
            title = habit.get_title_text()
            if title in next_task_titles:
                print(f"Habit task {title} is already exists.")
                continue
            habit_todo_task = TaskFactory.create_todo_task(
                title=title,
                task_kind_type=TaskKindType.HABIT,
                start_date=date,
                blocks=habit.block_children,
                habit_relation=habit.id,
            )
            self._lotion.create_page(habit_todo_task)
            print(f"Create task: {habit_todo_task.get_title_text()}")


if __name__ == "__main__":
    # python -m notion_api.usecase.create_routine_task_use_case
    from task.task_repository_impl import TaskRepositoryImpl

    task_repository = TaskRepositoryImpl()
    usecase = CreateRoutineTaskUseCase(task_repository=task_repository)
    usecase.execute(date_=jst_tommorow().date())
    # usecase._execute_habits(date=jst_tommorow().date())
