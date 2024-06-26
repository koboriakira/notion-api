import logging

from notion_client_wrapper.client_wrapper import ClientWrapper
from task.infrastructure.task_repository_impl import TaskRepositoryImpl
from usecase.move_tasks_to_backup_usecase import MoveTasksToBackupUsecase
from util.environment import Environment
from util.error_reporter import ErrorReporter

# ログ
logging.basicConfig(level=logging.INFO)
if Environment.is_dev():
    logging.basicConfig(level=logging.DEBUG)


def handler(event: dict, context: dict) -> None:  # noqa: ARG001
    try:
        task_repository = TaskRepositoryImpl(
            notion_client_wrapper=ClientWrapper.get_instance(),
        )
        usecase = MoveTasksToBackupUsecase(
            task_repository=task_repository,
        )
        usecase.execute()
    except:
        ErrorReporter().execute()
        raise


if __name__ == "__main__":
    handler({}, {})
