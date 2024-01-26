from datetime import date, timedelta
import logging
from interface import daily_log
from util.environment import Environment

# ログ
logging.basicConfig(level=logging.INFO)
if Environment.is_dev():
    logging.basicConfig(level=logging.DEBUG)

def handler(event, context):
    next_week_day = date.today() + timedelta(days=7)
    daily_log.create_daily_log(target_date=next_week_day)
