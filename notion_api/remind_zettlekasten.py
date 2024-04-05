import logging
import os

from slack_sdk import WebClient

from notion_client_wrapper.client_wrapper import ClientWrapper
from usecase.remind_zettlekasten_use_case import RemindZettlekastenUseCase
from util.environment import Environment
from util.error_reporter import ErrorReporter
from zettlekasten.infrastructure.zettlekasten_repository_impl import ZettlekastenRepositoryImpl

# ログ
logging.basicConfig(level=logging.INFO)
if Environment.is_dev():
    logging.basicConfig(level=logging.DEBUG)


def handler(event: dict, context: dict) -> dict:  # noqa: ARG001
    try:
        slack_client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])
        zettlekasten_repository = ZettlekastenRepositoryImpl(client=ClientWrapper.get_instance())
        usecase = RemindZettlekastenUseCase(
            zettlekasten_repository=zettlekasten_repository,
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
