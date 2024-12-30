import logging

from task.task_repository_impl import TaskRepositoryImpl
from usecase.create_routine_task_use_case import CreateRoutineTaskUseCase
from util.datetime import jst_today
from util.environment import Environment
from util.error_reporter import ErrorReporter

task_repository = TaskRepositoryImpl()
usecase = CreateRoutineTaskUseCase(task_repository=task_repository)

# ログ
logging.basicConfig(level=logging.INFO)
if Environment.is_dev():
    logging.basicConfig(level=logging.DEBUG)


def handler(event: dict, context: dict) -> None:  # noqa: ARG001
    try:
        usecase.execute(date_=jst_today())
    except Exception:  # noqa: BLE001
        ErrorReporter().execute()


if __name__ == "__main__":
    # python -m notion_api.create_routine_task
    handler({}, {})
