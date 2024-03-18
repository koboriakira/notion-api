import logging

from interface import daily_log
from util.environment import Environment

# ログ
logging.basicConfig(level=logging.INFO)
if Environment.is_dev():
    logging.basicConfig(level=logging.DEBUG)

def handler(event: dict, context:dict) -> dict:  # noqa: ARG001
    daily_log.collect_updated_pages()
    return {
        "statusCode": 200,
    }

if __name__ == "__main__":
    # python -m notion_api.collect_updated_pages
    handler()
