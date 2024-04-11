from dataclasses import dataclass
from datetime import date

from common.domain.tag_relation import TagRelation
from daily_log.domain.daily_goal import DailyGoal
from daily_log.domain.daily_log import DailyLog
from daily_log.domain.daily_log_date import DailyLogDate
from daily_log.domain.daily_log_title import DailyLogTitle
from daily_log.domain.daily_retro_comment import DailyRetroComment
from daily_log.domain.previous_relation import PreviousRelation
from daily_log.domain.weekly_log_relation import WeeklyLogRelation
from notion_client_wrapper.block.block import Block
from notion_client_wrapper.page.page_id import PageId
from notion_client_wrapper.properties.cover import Cover
from notion_client_wrapper.properties.properties import Properties
from notion_client_wrapper.properties.property import Property


@dataclass
class DailyLogBuilder:
    properties: list[Property]
    blocks: list[Block]
    cover: Cover | None

    @staticmethod
    def of(
        date_: date,
        blocks: list[Block] | None = None,
    ) -> "DailyLogBuilder":
        blocks = blocks or []
        properties = [
            DailyLogTitle.from_date(date_=date_),
            DailyLogDate.create(date_=date_),
        ]
        return DailyLogBuilder(properties=properties, blocks=blocks, cover=None)

    def build(self) -> DailyLog:
        return DailyLog(properties=Properties(self.properties), block_children=self.blocks, cover=self.cover)

    def add_daily_goal(self, daily_goal: str | DailyGoal) -> "DailyLogBuilder":
        daily_goal = daily_goal if isinstance(daily_goal, DailyGoal) else DailyGoal.from_plain_text(text=daily_goal)
        self.properties.append(daily_goal)
        return self

    def add_daily_retro_comment(self, daily_retro_comment: str | DailyRetroComment) -> "DailyLogBuilder":
        daily_retro_comment = (
            daily_retro_comment
            if isinstance(daily_retro_comment, DailyRetroComment)
            else DailyRetroComment.from_plain_text(text=daily_retro_comment)
        )
        self.properties.append(daily_retro_comment)
        return self

    def add_weekly_log_relation(self, weekly_log_relation: list[PageId] | WeeklyLogRelation) -> "DailyLogBuilder":
        weekly_log_relation = (
            weekly_log_relation
            if isinstance(weekly_log_relation, WeeklyLogRelation)
            else WeeklyLogRelation.from_id_list(id_list=weekly_log_relation)
        )
        self.properties.append(weekly_log_relation)
        return self

    def add_previous_relation(self, previous_relation: list[PageId] | PreviousRelation) -> "DailyLogBuilder":
        previous_relation = (
            previous_relation
            if isinstance(previous_relation, PreviousRelation)
            else PreviousRelation.from_id_list(id_list=previous_relation)
        )
        self.properties.append(previous_relation)
        return self

    def add_tag_relation(self, tag_relation: list[PageId] | TagRelation) -> "DailyLogBuilder":
        tag_relation = (
            tag_relation if isinstance(tag_relation, TagRelation) else TagRelation.from_id_list(id_list=tag_relation)
        )
        self.properties.append(tag_relation)
        return self

    def add_cover(self, cover: list[PageId] | TagRelation) -> "DailyLogBuilder":
        self.cover = cover if isinstance(cover, Cover) else Cover.from_external_url(cover)
        return self

    def add_block(self, block: Block) -> "DailyLogBuilder":
        self.blocks.append(block)
        return self
