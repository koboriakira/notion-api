from lotion import notion_database, notion_prop
from lotion.base_page import BasePage
from lotion.properties import Date, Title

from common.value.database_type import DatabaseType
from daily_log.isoweek import Isoweek


@notion_prop("名前")
class WeeklyLogTitle(Title):
    @staticmethod
    def from_isoweek(isoweek: Isoweek) -> "WeeklyLogTitle":
        return WeeklyLogTitle.from_plain_text(str(isoweek))


@notion_prop("期間")
class Range(Date):
    @staticmethod
    def from_isoweek(isoweek: Isoweek) -> "Range":
        return Range.from_range(isoweek.start_date, isoweek.end_date)


@notion_database(DatabaseType.WEEKLY_LOG.value)
class WeeklyLog(BasePage):
    title: WeeklyLogTitle
    range: Range

    @staticmethod
    def generate(isoweek: Isoweek) -> "WeeklyLog":
        return WeeklyLog.create([WeeklyLogTitle.from_isoweek(isoweek), Range.from_isoweek(isoweek)])
