import logging

from usecase.collect_updated_pages_usecase import CollectUpdatedPagesUsecase
from util.environment import Environment
from util.error_reporter import ErrorReporter

# ログ
logging.basicConfig(level=logging.INFO)
if Environment.is_dev():
    logging.basicConfig(level=logging.DEBUG)

def handler(event: dict, context:dict) -> dict:  # noqa: ARG001
    try:
        usecase = CollectUpdatedPagesUsecase()
        usecase.execute()
        return {
            "statusCode": 200,
        }
    except:
        ErrorReporter().report_error()
        raise

if __name__ == "__main__":
    # python -m notion_api.collect_updated_pages
    handler()
