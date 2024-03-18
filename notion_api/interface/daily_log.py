from datetime import date, datetime

from custom_logger import get_logger
from usecase.collect_updated_pages_usecase import CollectUpdatedPagesUsecase
from usecase.create_daily_log_usecase import CreateDailyLogUsecase
from util.datetime import jst_now

logger = get_logger(__name__)

def create_daily_log(target_date: date|None = None) -> None:
    target_date = target_date or jst_now()
    usecase = CreateDailyLogUsecase()
    usecase.handle(
        year=target_date.year,
        isoweeknum=target_date.isocalendar()[1],
        )

def collect_updated_pages(target_datetime: datetime | None = None) -> None:
    usecase = CollectUpdatedPagesUsecase()
    usecase.execute(target_datetime=target_datetime)
