from datetime import date, timedelta

from lotion import Lotion

from external_calendar.infrastructure.google_calendar_api import GoogleCalendarApi
from external_calendar.service.external_calendar_service import ExternalCalendarService
from notion_databases.task import Task
from notion_databases.task_prop.task_kind import TaskKindType
from notion_databases.task_prop.task_status import TaskStatusType
from task.task_factory import TaskFactory
from task.task_repository import TaskRepository
from task.task_repository_impl import TaskRepositoryImpl
from util.datetime import jst_tommorow


class SyncExternalCalendarUsecase:
    def __init__(
        self,
        task_repository: TaskRepository,
        external_calendar_service: ExternalCalendarService,
    ) -> None:
        self._lotion = Lotion.get_instance()
        self._task_repository = task_repository
        self._external_calendar_service = external_calendar_service

    def execute(self, date_: date) -> list[Task]:
        # 指定された日付から3日分の予定を取得
        tasks: list[Task] = []
        for _ in range(3):
            self._remove_scheduled_tasks(date_=date_)
            tasks.extend(self._sub_execute(date_=date_))
            date_ = date_ + timedelta(days=1)
        return tasks

    def _remove_scheduled_tasks(self, date_: date) -> None:
        scheduled_tasks = self._task_repository.search(
            kind_type_list=[TaskKindType.SCHEDULE],
            status_list=[TaskStatusType.TODO],
        )
        for task in scheduled_tasks:
            if not task.start_datetime:
                continue
            if task.start_datetime.date() == date_:
                print(f"Remove scheduled task: {task.get_title_text()}")
                self._lotion.remove_page(task.id)

    def _sub_execute(self, date_: date) -> list[Task]:
        events = self._external_calendar_service.get_events(
            date_=date_,
            excludes_past_events=True,
        )

        tasks: list[Task] = []
        for event in events.value:
            title = f"【{event.category.value}】{event.title}"
            task = self._lotion.create_page(
                TaskFactory.create_todo_task(
                    title=title,
                    task_kind_type=TaskKindType.SCHEDULE,
                    start_date=event.start,
                    end_date=event.end,
                ),
            )
            print(f"Create scheduled task: {task.get_title_text()}")
            tasks.append(task)
        return tasks


if __name__ == "__main__":
    # python -m notion_api.usecase.task.sync_external_calendar_usecase

    task_repository = TaskRepositoryImpl()
    external_calendar_service = ExternalCalendarService(
        api=GoogleCalendarApi(),
    )
    suite = SyncExternalCalendarUsecase(
        task_repository=task_repository,
        external_calendar_service=external_calendar_service,
    )
    print(suite.execute(date_=jst_tommorow().date()))
