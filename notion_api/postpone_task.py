import logging

from interface import task
from util.environment import Environment
from util.error_reporter import ErrorReporter

# ログ
logging.basicConfig(level=logging.INFO)
if Environment.is_dev():
    logging.basicConfig(level=logging.DEBUG)


def handler(event: dict, context: dict) -> None:  # noqa: ARG001
    try:
        task.postpone_to_next_day()
    except:
        ErrorReporter().execute()
        raise


if __name__ == "__main__":
    # python -m notion_api.postpone_task
    handler({}, {})
