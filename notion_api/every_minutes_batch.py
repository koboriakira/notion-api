import logging

from custom_logger import get_logger
from notion_client_wrapper.client_wrapper import ClientWrapper
from task.infrastructure.task_repository_impl import TaskRepositoryImpl
from usecase.clean_empty_title_page import CleanEmptyTitlePageUsecase
from usecase.task.do_tomorrow_usecase import DoTommorowUsecase
from util.environment import Environment
from util.error_reporter import ErrorReporter

logger = get_logger(__name__)
client = ClientWrapper.get_instance(logger=logger)
clean_empty_title_page_usecase = CleanEmptyTitlePageUsecase(client=client, logger=logger)
task_repository = TaskRepositoryImpl(notion_client_wrapper=client)
do_tomorrow_usecase = DoTommorowUsecase(task_repository=task_repository)


# ログ
logging.basicConfig(level=logging.INFO)
if Environment.is_dev():
    logging.basicConfig(level=logging.DEBUG)


def handler(event: dict, context: dict) -> None:
    try:
        logger.info("タイトルが空のページを削除")
        clean_empty_title_page_usecase.handle()
        logger.info("「明日やる」が有効になっているタスクを翌日に更新")
        do_tomorrow_usecase.execute()
    except:
        ErrorReporter().execute()
        raise


if __name__ == "__main__":
    # python -m notion_api.every_minutes_batch
    handler({}, {})
