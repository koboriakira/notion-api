import contextlib

from common.value.database_type import DatabaseType
from daily_log.domain.daily_log_repository import DailyLogRepository, ExistedDailyLogError
from daily_log.value.isoweek import Isoweek
from lotion import Lotion
from lotion.page import PageId
from lotion.properties Date, Title


class CreateDailyLogUsecase:
    def __init__(self, client: Lotion, daily_log_repository: DailyLogRepository) -> None:
        self.client = client
        self._daily_log_repository = daily_log_repository

    def handle(self, isoweek: Isoweek) -> None:
        # ウィークリーログを作成
        weekly_log_entity = self._create_weekly_log_page(isoweek)
        weekly_log_id = PageId(weekly_log_entity["id"])

        # デイリーログを作成
        for date_ in isoweek.date_range():
            with contextlib.suppress(ExistedDailyLogError):
                self._daily_log_repository.create(date_=date_, weekly_log_id=weekly_log_id)

    def _find_weekly_log(self, year: int, isoweeknum: int) -> dict | None:
        title = f"{year}-Week{isoweeknum}"
        weekly_log = self.client.find_page_by_title(
            database_id=DatabaseType.WEEKLY_LOG.value,
            title=title,
        )
        if weekly_log is None:
            return None
        title = weekly_log.get_title()
        goal = weekly_log.get_text(name="目標")
        return {
            "id": weekly_log.id,
            "url": weekly_log.url,
            "title": title.text,
            "goal": goal.text,
        }

    def _create_weekly_log_page(self, isoweek: Isoweek) -> dict:
        weekly_log_entity = self._find_weekly_log(isoweek.year, isoweek.isoweeknum)
        if weekly_log_entity is not None:
            return weekly_log_entity

        return self.client.create_page_in_database(
            database_id=DatabaseType.WEEKLY_LOG.value,
            properties=[
                Title.from_plain_text(name="名前", text=str(isoweek)),
                Date.from_range(name="期間", start=isoweek.start_date, end=isoweek.end_date),
            ],
        )
