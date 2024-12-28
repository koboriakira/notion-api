from abc import ABCMeta, abstractmethod
from datetime import date

from notion_databases.daily_log import DailyLog


class ExistedDailyLogError(Exception):
    def __init__(self, date_: date) -> None:
        self.date_ = date_
        super().__init__(f"Existed daily log for {date_}")


class NotFoundDailyLogError(Exception):
    def __init__(self, date_: date) -> None:
        self.date_ = date_
        super().__init__(f"Not found daily log for {date_}")


class DailyLogRepository(metaclass=ABCMeta):
    """デイリーログのリポジトリクラス"""

    @abstractmethod
    def find(self, date: date) -> DailyLog:
        """指定された日付のデイリーログを取得する

        Args:
            date: 検索する日付

        Returns:
            DailyLog: 指定された日付のデイリーログ。存在しない場合はNoneを返す

        Raises:
            NotFoundDailyLogError: 指定された日付のデイリーログが存在しない場合
        """

    @abstractmethod
    def save(self, daily_log: DailyLog) -> DailyLog:
        """デイリーログを保存する

        Args:
            daily_log: 保存するデイリーログ

        Returns:
            DailyLog: 保存されたデイリーログ
        """

    @abstractmethod
    def create(self, date_: date, weekly_log_id: str) -> DailyLog:
        """デイリーログを新規作成する

        Args:
            date_: 作成するデイリーログの日付
            weekly_log_id: デイリーログが所属する週報のID

        Returns:
            DailyLog: 新しく作成されたデイリーログ

        Raises:
            ExistedDailyLogError: 既にデイリーログが存在する場合
            NotFoundDailyLogError: 前日のデイリーログが存在しない場合
        """
