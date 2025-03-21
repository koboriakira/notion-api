import logging

from lotion import Lotion

from custom_logger import get_logger
from task.task_repository_impl import TaskRepositoryImpl
from usecase.clean_empty_title_page import CleanEmptyTitlePageUsecase
from usecase.shopping.reset_shopping_list_usecase import ResetShoppingListUseCase
from usecase.task.maintain_tasks_usecase import MaintainTasksUsecase
from usecase.task.start_task_usecase import StartTaskUsecase
from util.environment import Environment
from util.error_reporter import ErrorReporter

logger = get_logger(__name__)
client = Lotion.get_instance(logger=logger)
clean_empty_title_page_usecase = CleanEmptyTitlePageUsecase(client=client, logger=logger)
task_repository = TaskRepositoryImpl(notion_client_wrapper=client)
maintain_tasks_usecase = MaintainTasksUsecase()
reset_shopping_list_usecase = ResetShoppingListUseCase()
start_task_usecase = StartTaskUsecase(task_repository=task_repository)

# ログ
logging.basicConfig(level=logging.INFO)
if Environment.is_dev():
    logging.basicConfig(level=logging.DEBUG)


def handler(event: dict, context: dict) -> None:
    try:
        logger.info("更新されたタスクに関して自動調整")
        maintain_tasks_usecase.execute()

        logger.info("タイトルが空のページを削除")
        clean_empty_title_page_usecase.handle()

        logger.info("買い物リストの購入ステータスをリセット")
        reset_shopping_list_usecase.execute()

    except Exception as e:
        ErrorReporter().execute(error=e)
        raise


if __name__ == "__main__":
    # python -m notion_api.every_minutes_batch
    handler({}, {})
