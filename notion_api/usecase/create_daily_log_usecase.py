import contextlib

from lotion import Lotion

from daily_log.daily_log_repository import DailyLogRepository, ExistedDailyLogError
from daily_log.isoweek import Isoweek
from notion_databases.weekly_log import WeeklyLog, WeeklyLogTitle


class CreateDailyLogUsecase:
    def __init__(self, client: Lotion, daily_log_repository: DailyLogRepository) -> None:
        self.client = client
        self._daily_log_repository = daily_log_repository

    def handle(self, isoweek: Isoweek) -> None:
        # ウィークリーログを作成
        weekly_log = self._create_weekly_log_page(isoweek)

        # デイリーログを作成
        for date_ in isoweek.date_range():
            with contextlib.suppress(ExistedDailyLogError):
                self._daily_log_repository.create(date_=date_, weekly_log_id=weekly_log.id)

    def _find_weekly_log(self, isoweek: Isoweek) -> WeeklyLog | None:
        title = WeeklyLogTitle.from_isoweek(isoweek)
        return self.client.find_page(WeeklyLog, title)

    def _create_weekly_log_page(self, isoweek: Isoweek) -> WeeklyLog:
        weekly_log = self._find_weekly_log(isoweek)
        if weekly_log is not None:
            return weekly_log

        weekly_log = WeeklyLog.generate(isoweek)
        return self.client.create_page(weekly_log)
