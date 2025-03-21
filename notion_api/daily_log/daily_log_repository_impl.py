from datetime import date, timedelta
from logging import Logger, getLogger

from lotion import Lotion

from common.value.database_type import DatabaseType
from daily_log.daily_log_builder import DailyLogBuilder
from daily_log.daily_log_repository import DailyLogRepository, NotFoundDailyLogError
from notion_databases.daily_log import DailyLog, DailyLogTitle


class DailyLogRepositoryImpl(DailyLogRepository):
    DATABASE_ID = DatabaseType.DAILY_LOG.value

    def __init__(self, client: Lotion, logger: Logger | None = None) -> None:
        self._client = client
        self._logger = logger or getLogger(__name__)

    def find(self, date: date) -> DailyLog:
        daily_log = self._find_daily_log(date_=date)
        if daily_log is None:
            raise NotFoundDailyLogError(date)
        return daily_log

    def save(self, daily_log: DailyLog) -> DailyLog:
        return self._client.create_page(daily_log)

    def create(self, date_: date, weekly_log_id: str) -> DailyLog:
        created_daily_log = self._find_daily_log(date_)
        if created_daily_log is not None:
            return created_daily_log

        yesterday = date_ - timedelta(days=1)
        yesterday_daily_log = self.find(yesterday)

        daily_log = (
            DailyLogBuilder.of(date_=date_)
            .add_weekly_log_relation(weekly_log_page_id=weekly_log_id)
            .add_previous_relation(previous_page_id=yesterday_daily_log.id)
            # .add_random_cover()
            .build()
        )
        return self.save(daily_log)

    def _find_daily_log(self, date_: date) -> DailyLog | None:
        title = DailyLogTitle.from_date(date_)
        return self._client.find_page(DailyLog, title)
