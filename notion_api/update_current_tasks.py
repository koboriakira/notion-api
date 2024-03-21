import logging

from interface import batch
from util.environment import Environment
from util.error_reporter import ErrorReporter

# ログ
logging.basicConfig(level=logging.INFO)
if Environment.is_dev():
    logging.basicConfig(level=logging.DEBUG)

def handler(event:dict, context:dict) -> None:  # noqa: ARG001
    try:
        batch.update_current_tasks()
    except:
        ErrorReporter().execute()
        raise

if __name__ == "__main__":
    handler({}, {})
