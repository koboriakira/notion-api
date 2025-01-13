from enum import Enum

from lotion import notion_database, notion_prop
from lotion.base_page import BasePage
from lotion.properties import MultiSelect, Relation, Text

from common.value.database_type import DatabaseType


@notion_prop("名前")
class HabitName(Text):
    pass


# 頻度
class HabitFrequencyType(Enum):
    SUNDAY = "日"
    MONDAY = "月"
    TUESDAY = "火"
    WEDNESDAY = "水"
    THURSDAY = "木"
    FRIDAY = "金"
    SATURDAY = "土"


@notion_prop("頻度")
class HabitFrequency(MultiSelect):
    def to_enum(self) -> list[HabitFrequencyType]:
        return [HabitFrequencyType(v.name) for v in self.values]


@notion_prop("目標")
class GoalRelation(Relation):
    pass


@notion_database(DatabaseType.HABIT_TRACKER.value)
class HabitTracker(BasePage):
    task_name: HabitName
    frequency: HabitFrequency
    goal_relation: GoalRelation
