import logging
from datetime import date

from interface import task
from util.environment import Environment
from util.error_reporter import ErrorReporter

# ログ
logging.basicConfig(level=logging.INFO)
if Environment.is_dev():
    logging.basicConfig(level=logging.DEBUG)

def handler(event: dict, context:dict) -> None:  # noqa: ARG001
    try:
        date_str: str | None = event.get("date")
        target_date = date.fromisoformat(date_str) if date_str else None
        return task.postpone_to_next_day(date=target_date)
    except:
        ErrorReporter().report_error()
        raise
