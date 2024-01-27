from datetime import date as Date
from typing import Optional
from custom_logger import get_logger
from usecase.create_daily_log_usecase import CreateDailyLogUsecase
from usecase.collect_updated_pages_usecase import CollectUpdatedPagesUsecase

logger = get_logger(__name__)

def create_daily_log(target_date: Date = Date.today()):
    usecase = CreateDailyLogUsecase()
    usecase.handle(year=target_date.year, isoweeknum=target_date.isocalendar()[1])

def collect_updated_pages(date: Optional[Date] = None):
    usecase = CollectUpdatedPagesUsecase()
    usecase.execute(date)

if __name__ == "__main__":
    # python -m interface.daily_log
    collect_updated_pages(date=Date(2024, 1, 26))
