from datetime import date

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
            for scheduled_task in scheduled_tasks:
                if scheduled_task.title == title:
                    self._task_repository.delete(scheduled_task)
                    break
            task = self._task_repository.save(
                TaskFactory.create_scheduled_task(
                    title=title,
                    start_date=event.start,
                    end_date=event.end,
                ),
            )
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
    print(suite.execute(date_=jst_now().date()))
