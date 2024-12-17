from external_calendar.infrastructure.google_calendar_api import GoogleCalendarApi
from external_calendar.service.external_calendar_service import ExternalCalendarService
from task.infrastructure.task_repository_impl import TaskRepositoryImpl
from usecase.task.sync_external_calendar_usecase import SyncExternalCalendarUsecase
from util.datetime import jst_now
from util.error_reporter import ErrorReporter


def handler(event: dict, context: dict) -> None:
    try:
        task_repository = TaskRepositoryImpl()
        external_calendar_service = ExternalCalendarService(
            api=GoogleCalendarApi(),
        )
        suite = SyncExternalCalendarUsecase(
            task_repository=task_repository,
            external_calendar_service=external_calendar_service,
        )
        print(suite.execute(date_=jst_now().date()))

    except Exception as e:
        ErrorReporter().execute(error=e)
        raise


if __name__ == "__main__":
    # python -m notion_api.sync_external_calendar
    handler({}, {})
