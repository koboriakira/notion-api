import logging
from datetime import timedelta

from interface import daily_log
from util.datetime import jst_now
from util.environment import Environment
from util.error_reporter import ErrorReporter

# ログ
logging.basicConfig(level=logging.INFO)
if Environment.is_dev():
    logging.basicConfig(level=logging.DEBUG)

def handler(event:dict, context:dict) -> None:  # noqa: ARG001
    try:
        next_week_day = jst_now().date() + timedelta(days=7)
        daily_log.create_daily_log(target_date=next_week_day)
    except:
        ErrorReporter().report_error()
        raise
