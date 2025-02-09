from datetime import date, timedelta

from lotion import Lotion
from lotion.filter import Builder, Cond

from notion_databases.task import Task, TaskKind
from notion_databases.task_prop.task_start_date import TaskStartDate


class ReviewThisWeekMainTasksUsecase:
    def __init__(self, lotion: Lotion | None = None) -> None:
        self._lotion = lotion or Lotion.get_instance()

    def execute(self, date: date) -> None:
        filter_builder = (
            Builder.create()
            .add(TaskKind.thisweek(), Cond.EQUALS)
            .add(TaskStartDate.from_start_date(date - timedelta(days=7)), Cond.ON_OR_AFTER)
            .add(TaskStartDate.from_start_date(date), Cond.ON_OR_BEFORE)
        )
        tasks = self._lotion.retrieve_pages(
            cls=Task,
            filter_param=filter_builder.build(),
            include_children=False,
        )

        done_tasks = [t for t in tasks if t.is_completed]
        notdone_tasks = [t for t in tasks if not t.is_completed]
        for task in done_tasks:
            print(task.get_title_text())
        print("-----------------------")
        for task in notdone_tasks:
            print(task.get_title_text())


if __name__ == "__main__":
    # python -m notion_api.usecase.task.review_this_week_main_tasks_usecase
    suite = ReviewThisWeekMainTasksUsecase()
    suite.execute(date.today())
