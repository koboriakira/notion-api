from datetime import date
from logging import Logger, getLogger

from common.value.database_type import DatabaseType
from daily_log.domain.daily_log import DailyLog
from daily_log.domain.daily_log_repository import DailyLogRepository
from notion_client_wrapper.client_wrapper import ClientWrapper
from notion_client_wrapper.filter.filter_builder import FilterBuilder


class DailyLogRepositoryImpl(DailyLogRepository):
    DATABASE_ID = DatabaseType.DAILY_LOG.value

    def __init__(self, client: ClientWrapper, logger: Logger | None = None) -> None:
        self._client = client
        self._logger = logger or getLogger(__name__)

    def find(self, date: date) -> DailyLog | None:
        filter_param = FilterBuilder.build_title_equal_condition(title=date.isoformat())
        daily_logs: list[DailyLog] = self._client.retrieve_database(
            database_id=self.DATABASE_ID,
            filter_param=filter_param,
            page_model=DailyLog,
        )
        if len(daily_logs) == 0:
            return None
        return daily_logs[0]

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
