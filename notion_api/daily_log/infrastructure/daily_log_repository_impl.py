from datetime import date, datetime, timedelta
from logging import Logger, getLogger

from lotion import Lotion
from lotion.base_page import BasePage
from lotion.page.page_id import PageId

from common.value.database_type import DatabaseType
from daily_log.domain.daily_log import DailyLog
from daily_log.domain.daily_log_builder import DailyLogBuilder
from daily_log.domain.daily_log_repository import DailyLogRepository, ExistedDailyLogError, NotFoundDailyLogError


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
        result = self._client.create_page_in_database(
            database_id=self.DATABASE_ID,
            cover=daily_log.cover,
            properties=daily_log.properties.values,
            blocks=daily_log.block_children,
        )
        daily_log.update_id_and_url(
            page_id=result.page_id.value,
            url=result.url,
        )
        return daily_log

    def create(self, date_: date, weekly_log_id: PageId) -> DailyLog:
        assert not isinstance(date_, datetime)
        assert isinstance(weekly_log_id, PageId)

        if self._find_daily_log(date_) is not None:
            raise ExistedDailyLogError(date_)

        yesterday = date_ - timedelta(days=1)
        yesterday_daily_log = self.find(yesterday)

        daily_log = (
            DailyLogBuilder.of(date_=date_)
            .add_weekly_log_relation(weekly_log_page_id=weekly_log_id)
            .add_previous_relation(previous_page_id=yesterday_daily_log.page_id)
            # .add_random_cover()
            .build()
        )
        return self.save(daily_log)

    def _find_daily_log(self, date_: date) -> DailyLog | None:
        base_page = self._client.find_page_by_title(
            database_id=self.DATABASE_ID,
            title=date_.isoformat(),
        )
        if base_page is None:
            return None
        return self._cast(base_page)

    def _cast(self, base_page: BasePage) -> DailyLog:
        return DailyLog(
            properties=base_page.properties,
            block_children=base_page.block_children,
            id_=base_page.id_,
            url=base_page.url,
            created_time=base_page.created_time,
            last_edited_time=base_page.last_edited_time,
            _created_by=base_page._created_by,
            _last_edited_by=base_page._last_edited_by,
            cover=base_page.cover,
            icon=base_page.icon,
            archived=base_page.archived,
            parent=base_page.parent,
        )
