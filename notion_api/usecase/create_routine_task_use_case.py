from datetime import date, timedelta

from lotion import Lotion

from notion_databases.routine_task import RoutineTask
from notion_databases.task import TaskKind
from notion_databases.task_prop.task_kind import TaskKindType
from notion_databases.task_prop.task_status import TaskStatusType
from task.task_factory import TaskFactory
from task.task_repository import TaskRepository
from util.datetime import jst_tommorow


def create_routine_kind_type() -> TaskKind:
    # 高速化のため、事前に取得しておく
    return TaskKind(
        name="タスク種別",
        selected_name="ルーティン",
        selected_id="44c37655-c056-49d2-8441-61929400f6a3",
        selected_color="default",
    )


class CreateRoutineTaskUseCase:
    def __init__(self, task_repository: TaskRepository, lotion: Lotion | None = None) -> None:
        self.task_repository = task_repository
        self._lotion = lotion or Lotion.get_instance()

    def execute(self, date_: date) -> None:
        routine_tasks = self._lotion.retrieve_pages(RoutineTask)
        next_tasks = self.task_repository.search(
            status_list=[TaskStatusType.TODO, TaskStatusType.IN_PROGRESS],
            kind_type_list=[TaskKindType.ROUTINE],
            start_datetime=date_,
            start_datetime_end=date_ + timedelta(days=90),
        )
        next_task_titles = [task.get_title().text for task in next_tasks]

        for routine_task in routine_tasks:
            title = routine_task.get_title_text()
            if title in next_task_titles:
                print(f"Routine task {title} is already exists.")
                continue
            start_date, end_date = routine_task.get_next_schedule(basis_date=date_)
            routine_todo_task = TaskFactory.create_todo_task(
                title=title,
                start_date=start_date,
                end_date=end_date,
                blocks=routine_task.block_children if routine_task.get_title_text() != "買い物 & 料理" else [],
            )
            routine_todo_task.set_prop(create_routine_kind_type())
            print(f"Create task: {routine_todo_task.get_title_text()}")
            self._lotion.create_page(routine_todo_task)


if __name__ == "__main__":
    # python -m notion_api.usecase.create_routine_task_use_case
    from task.task_repository_impl import TaskRepositoryImpl

    task_repository = TaskRepositoryImpl()
    usecase = CreateRoutineTaskUseCase(task_repository=task_repository)
    usecase.execute(date_=jst_tommorow().date())
