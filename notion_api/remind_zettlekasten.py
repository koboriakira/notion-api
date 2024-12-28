import logging
import os

from slack_sdk import WebClient

from usecase.remind_zettlekasten_use_case import RemindZettlekastenUseCase
from util.environment import Environment
from util.error_reporter import ErrorReporter

# ログ
logging.basicConfig(level=logging.INFO)
if Environment.is_dev():
    logging.basicConfig(level=logging.DEBUG)


def handler(event: dict, context: dict) -> dict:  # noqa: ARG001
    try:
        slack_client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])
        usecase = RemindZettlekastenUseCase(
            slack_client=slack_client,
        )
        usecase.execute()
        return {
            "statusCode": 200,
        }
    except:
        ErrorReporter().execute()
        raise


if __name__ == "__main__":
    # python -m notion_api.remind_zettlekasten
    handler({}, {})
