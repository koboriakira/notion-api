import logging
from typing import Optional
from datetime import date as Date
from interface import daily_log
from util.environment import Environment

# ログ
logging.basicConfig(level=logging.INFO)
if Environment.is_dev():
    logging.basicConfig(level=logging.DEBUG)

def handler(event: dict, context):
    date_str: Optional[str] = event.get("date")
    date = Date.fromisoformat(date_str) if date_str else None
    daily_log.collect_updated_pages(date=date)

if __name__ == "__main__":
    # python -m collect_updated_pages
    handler(event={"date": "2024-01-31"}, context={})
