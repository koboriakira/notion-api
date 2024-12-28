from dataclasses import dataclass
from datetime import date

from lotion.block import Block
from lotion.properties import Cover, Properties, Property

from common.domain.tag_relation import TagRelation
from daily_log.domain.daily_log import (
    DailyGoal,
    DailyLog,
    DailyLogDate,
    DailyLogTitle,
    DailyRetroComment,
    PreviousRelation,
    WeeklyLogRelation,
)


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
            DailyLogDate.from_start_date(date_),
        ]
        return DailyLogBuilder(properties=properties, blocks=blocks, cover=None)

    def build(self) -> DailyLog:
        return DailyLog(properties=Properties(self.properties), block_children=self.blocks, cover=self.cover)

    def add_daily_goal(self, daily_goal: str) -> "DailyLogBuilder":
        self.properties.append(DailyGoal.from_plain_text(daily_goal))
        return self

    def add_daily_retro_comment(self, daily_retro_comment: str) -> "DailyLogBuilder":
        self.properties.append(DailyRetroComment.from_plain_text(text=daily_retro_comment))
        return self

    def add_weekly_log_relation(self, weekly_log_page_id: str) -> "DailyLogBuilder":
        self.properties.append(WeeklyLogRelation.from_id_list(id_list=[weekly_log_page_id]))
        return self

    def add_previous_relation(self, previous_page_id: str) -> "DailyLogBuilder":
        self.properties.append(PreviousRelation.from_id_list(id_list=[previous_page_id]))
        return self

    def add_tag_relation(self, tag_relation: list[str]) -> "DailyLogBuilder":
        self.properties.append(TagRelation.from_id_list(tag_relation))
        return self

    # def add_random_cover(self) -> "DailyLogBuilder":
    #     self.cover = Cover.random(query_words=["bird", "flower"])
    #     return self

    def add_cover(self, cover_url: str) -> "DailyLogBuilder":
        self.cover = Cover.from_external_url(cover_url)
        return self

    def add_block(self, block: Block) -> "DailyLogBuilder":
        self.blocks.append(block)
        return self
