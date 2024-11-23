from datetime import date, timedelta

from external_calendar.infrastructure.google_calendar_api import GoogleCalendarApi
from external_calendar.service.external_calendar_service import ExternalCalendarService
from task.domain.task import Task
from task.domain.task_kind import TaskKindType
from task.domain.task_repository import TaskRepository
from task.infrastructure.task_repository_impl import TaskRepositoryImpl
from task.task_factory import TaskFactory
from util.datetime import jst_now


class SyncExternalCalendarUsecase:
    def __init__(
        self,
        task_repository: TaskRepository,
        external_calendar_service: ExternalCalendarService,
    ) -> None:
        self._task_repository = task_repository
        self._external_calendar_service = external_calendar_service

    def execute(self, date_: date) -> list[Task]:
        # 指定された日付から3日分の予定を取得
        tasks: list[Task] = []
        for _ in range(3):
            tasks.extend(self._sub_execute(date_=date_))
            date_ = date_ + timedelta(days=1)
        return tasks

    def _sub_execute(self, date_: date) -> list[Task]:
        scheduled_tasks = self._task_repository.search(
            start_datetime=date_,
            start_datetime_end=date_,
            kind_type_list=[TaskKindType.SCHEDULE],
        )

        events = self._external_calendar_service.get_events(
            date_=date_,
            excludes_past_events=True,
        )

        tasks: list[Task] = []
        for event in events.value:
            title = f"【{event.category.value}】{event.title}"
            self._remove_if_exists(tasks=scheduled_tasks, title=title)

            task = self._task_repository.save(
                TaskFactory.create_scheduled_task(
                    title=title,
                    start_date=event.start,
                    end_date=event.end,
                ),
            )
            tasks.append(task)
        return tasks

    def _remove_if_exists(self, tasks: list[Task], title: str) -> None:
        for task in tasks:
            if task.title == title:
                self._task_repository.delete(task)
                return


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
    print(suite.execute(date_=jst_now().date()))
