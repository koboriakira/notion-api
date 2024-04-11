from datetime import date, timedelta
from logging import Logger, getLogger

from common.value.database_type import DatabaseType
from daily_log.domain.daily_log import DailyLog
from daily_log.domain.daily_log_builder import DailyLogBuilder
from daily_log.domain.daily_log_repository import DailyLogRepository, ExistedDailyLogError, NotFoundDailyLogError
from notion_client_wrapper.client_wrapper import ClientWrapper
from notion_client_wrapper.filter.filter_builder import FilterBuilder
from notion_client_wrapper.page.page_id import PageId


class DailyLogRepositoryImpl(DailyLogRepository):
    DATABASE_ID = DatabaseType.DAILY_LOG.value

    def __init__(self, client: ClientWrapper, logger: Logger | None = None) -> None:
        self._client = client
        self._logger = logger or getLogger(__name__)

    def find(self, date: date) -> DailyLog:
        daily_log = self._find_daily_log(date)
        if daily_log is None:
            raise NotFoundDailyLogError(date)
        return daily_log

    def save(self, daily_log: DailyLog) -> DailyLog:
        result = self._client.create_page_in_database(
            database_id=self.DATABASE_ID,
            cover=daily_log.cover,
            properties=daily_log.properties.values,
            blocks=daily_log.block_children,
        )
        daily_log.update_id_and_url(
            page_id=result["id"],
            url=result["url"],
        )
        return daily_log

    def create(self, date_: date, weekly_log_id: PageId) -> DailyLog:
        """デイリーログを新規作成する"""
        if self._find_daily_log(date_) is not None:
            raise ExistedDailyLogError(date_)

        yesterday_daily_log = self.find(date_ - timedelta(days=1))

        daily_log = (
            DailyLogBuilder.of(date_=date_)
            .add_weekly_log_relation(weekly_log_page_id=PageId(weekly_log_id))
            .add_previous_relation(previous_page_id=PageId(yesterday_daily_log.id))
            .add_random_cover()
            .build()
        )
        return self.save(daily_log)

    def _find_daily_log(self, date: date) -> DailyLog | None:
        filter_param = FilterBuilder.build_title_equal_condition(title=date.isoformat())
        daily_logs: list[DailyLog] = self._client.retrieve_database(
            database_id=self.DATABASE_ID,
            filter_param=filter_param,
            page_model=DailyLog,
        )
        if len(daily_logs) == 0:
            return None
        return daily_logs[0]
