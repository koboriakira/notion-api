from datetime import date

from lotion import notion_database, notion_prop
from lotion.base_page import BasePage
from lotion.properties import Date, Relation, Text, Title

from common.domain.tag_relation import TagRelation
from common.value.database_type import DatabaseType


@notion_prop("名前")
class DailyLogTitle(Title):
    @staticmethod
    def from_date(date_: date) -> "DailyLogTitle":
        return DailyLogTitle.from_plain_text(text=date_.isoformat())


@notion_prop("目標")
class DailyGoal(Text):
    pass


@notion_prop("日付")
class DailyLogDate(Date):
    pass


@notion_prop("ふりかえり")
class DailyRetroComment(Text):
    pass


@notion_prop("前日")
class PreviousRelation(Relation):
    pass


@notion_prop("💭 ウィークリーログ")
class WeeklyLogRelation(Relation):
    pass


@notion_database(DatabaseType.DAILY_LOG.value)
class DailyLog(BasePage):
    title: DailyLogTitle
    date: DailyLogDate
    retro_comment: DailyRetroComment
    tags: TagRelation
    previous_day: PreviousRelation
    goal: DailyGoal
    weekly_log: WeeklyLogRelation
