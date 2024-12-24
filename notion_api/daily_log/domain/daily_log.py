from dataclasses import dataclass
from datetime import date

from lotion.base_page import BasePage

from common.domain.tag_relation import TagRelation
from daily_log.domain.daily_goal import DailyGoal
from daily_log.domain.daily_log_date import DailyLogDate
from daily_log.domain.daily_retro_comment import DailyRetroComment
from daily_log.domain.previous_relation import PreviousRelation
from daily_log.domain.weekly_log_relation import WeeklyLogRelation


@dataclass
class DailyLog(BasePage):
    @property
    def weekly_log_relation(self) -> list[str]:
        return self.get_relation(name=WeeklyLogRelation.NAME).id_list

    @property
    def previous_relation(self) -> list[str]:
        return self.get_relation(name=PreviousRelation.NAME).id_list

    @property
    def tag_relation(self) -> list[str]:
        return self.get_relation(name=TagRelation.NAME).id_list

    @property
    def date(self) -> date | None:
        daily_log_date = self.get_date(name=DailyLogDate.NAME)
        if daily_log_date is None:
            msg = f"Date not found. page: {self.get_title_text()}"
            raise Exception(msg)
        return daily_log_date.start_date if daily_log_date is not None else None

    @property
    def goal(self) -> str:
        return self.get_text(name=DailyGoal.NAME).text

    @property
    def retro_comment(self) -> str:
        return self.get_text(name=DailyRetroComment.NAME).text
