from abc import ABCMeta, abstractmethod
from datetime import date

from daily_log.domain.daily_log import DailyLog
from notion_client_wrapper.page.page_id import PageId


class DailyLogRepository(metaclass=ABCMeta):
    @abstractmethod
    def find(self, date: date) -> DailyLog | None:
        """指定された日付のデイリーログを取得する"""

    @abstractmethod
    def save(self, daily_log: DailyLog) -> DailyLog:
        """デイリーログを保存する"""

    @abstractmethod
    def create(self, date_: date, weekly_log_id: PageId) -> DailyLog:
        """デイリーログを新規作成する"""
