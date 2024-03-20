import logging

from interface import batch
from util.environment import Environment
from util.error_reporter import ErrorReporter

# ログ
logging.basicConfig(level=logging.INFO)
if Environment.is_dev():
    logging.basicConfig(level=logging.DEBUG)

def handler(event: dict, context: dict) -> None:
    try:
        batch.clean_empty_title_page()
    except:
        ErrorReporter().report_error()
        raise
