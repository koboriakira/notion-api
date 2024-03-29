import logging

from injector.injector import Injector
from util.environment import Environment
from util.error_reporter import ErrorReporter

# ログ
logging.basicConfig(level=logging.INFO)
if Environment.is_dev():
    logging.basicConfig(level=logging.DEBUG)

use_case = Injector.get_create_tag_to_zettlekasten_use_case()

def handler(event:dict, context:dict) -> None:  # noqa: ARG001
    try:
        use_case.execute()
    except:
        ErrorReporter().execute()
        raise

if __name__ == "__main__":
    # python -m notion_api.handler.create_tag_to_zettlekasten
    handler({}, {})
