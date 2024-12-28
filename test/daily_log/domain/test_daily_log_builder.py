import sys
from datetime import date
from unittest import TestCase

from notion_api.daily_log.domain.daily_log_builder import DailyLogBuilder

sys.path.append("notion_api")
from lotion.page.page_id import PageId


class TestDailyLogBuilder(TestCase):
    def test_インスタンスの生成(self):
        # When
        weekly_log_page_id = PageId.dummy().value
        previous_page_id = PageId.dummy().value
        tag_page_id = PageId.dummy().value
        actual = (
            DailyLogBuilder.of(date_=date.fromisoformat("2024-02-13"))
            .add_daily_goal("目標")
            .add_daily_retro_comment("ふりかえり")
            .add_weekly_log_relation(weekly_log_page_id)
            .add_previous_relation(previous_page_id)
            .add_tag_relation([tag_page_id])
            .add_cover("https://example.com/cover.jpg")
            .build()
        )

        # Then
        self.assertEqual(actual.date.date, date.fromisoformat("2024-02-13"))
        self.assertEqual(actual.goal.text, "目標")
        self.assertEqual(actual.retro_comment.text, "ふりかえり")
        self.assertEqual(actual.weekly_log.id_list, [weekly_log_page_id])
        self.assertEqual(actual.previous_day.id_list, [previous_page_id])
        self.assertEqual(actual.tags.id_list, [tag_page_id])
        actual_external_url = actual.cover.external_url if actual.cover else None
        self.assertEqual(actual_external_url, "https://example.com/cover.jpg")
        self.assertEqual(actual.block_children, [])
