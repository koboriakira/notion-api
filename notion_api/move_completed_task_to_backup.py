import logging

from lotion import Lotion

from project.project_repository_impl import ProjectRepositoryImpl
from task.task_repository_impl import TaskRepositoryImpl
from usecase.move_tasks_to_backup_usecase import MoveTasksToBackupUsecase
from util.environment import Environment
from util.error_reporter import ErrorReporter

# ログ
logging.basicConfig(level=logging.INFO)
if Environment.is_dev():
    logging.basicConfig(level=logging.DEBUG)


def handler(event: dict, context: dict) -> None:  # noqa: ARG001
    try:
        notion_client = Lotion.get_instance()
        task_repository = TaskRepositoryImpl(notion_client_wrapper=notion_client)
        project_repository = ProjectRepositoryImpl(client=notion_client)
        usecase = MoveTasksToBackupUsecase(
            task_repository=task_repository,
            project_repository=project_repository,
        )
        usecase.execute()
    except:
        ErrorReporter().execute()
        raise


if __name__ == "__main__":
    # python -m notion_api.move_completed_task_to_backup
    handler({}, {})
