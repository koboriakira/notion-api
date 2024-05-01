import logging

from custom_logger import get_logger
from notion_client_wrapper.client_wrapper import ClientWrapper
from usecase.clean_empty_title_page import CleanEmptyTitlePageUsecase
from util.environment import Environment
from util.error_reporter import ErrorReporter

logger = get_logger(__name__)


# ログ
logging.basicConfig(level=logging.INFO)
if Environment.is_dev():
    logging.basicConfig(level=logging.DEBUG)


def handler(event: dict, context: dict) -> None:
    try:
        client = ClientWrapper.get_instance(logger=logger)
        usecase = CleanEmptyTitlePageUsecase(client=client, logger=logger)
        usecase.handle()
    except:
        ErrorReporter().execute()
        raise


if __name__ == "__main__":
    # python -m notion_api.clean_empty_title_page
    handler({}, {})
