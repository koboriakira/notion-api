from datetime import date as Date
from custom_logger import get_logger
from usecase.create_daily_log_usecase import CreateDailyLogUsecase

logger = get_logger(__name__)

def create_daily_log(target_date: Date = Date.today()):
    usecase = CreateDailyLogUsecase()
    usecase.handle(year=target_date.year, isoweeknum=target_date.isocalendar()[1])


if __name__ == "__main__":
    # python -m interface.daily_log
    create_daily_log()
