import sys
from datetime import date
from unittest import TestCase

from notion_api.daily_log.domain.daily_log_builder import DailyLogBuilder

sys.path.append("notion_api")
from notion_client_wrapper.page.page_id import PageId


class TestDailyLogBuilder(TestCase):
    def test_インスタンスの生成(self):
        # When
        weekly_log_page_id = PageId.dummy()
        previous_page_id = PageId.dummy()
        tag_page_id = PageId.dummy()
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
        self.assertEqual(actual.date, date.fromisoformat("2024-02-13"))
        self.assertEqual(actual.goal, "目標")
        self.assertEqual(actual.retro_comment, "ふりかえり")
        self.assertEqual(actual.weekly_log_relation, [weekly_log_page_id])
        self.assertEqual(actual.previous_relation, [previous_page_id])
        self.assertEqual(actual.tag_relation, [tag_page_id])
        self.assertEqual(actual.cover.external_url, "https://example.com/cover.jpg")
        self.assertEqual(actual.block_children, [])
