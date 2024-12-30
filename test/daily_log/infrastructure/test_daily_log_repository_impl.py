from datetime import date
from logging import Logger
from unittest import TestCase
from unittest.mock import Mock

import pytest
from lotion import Lotion

from daily_log.daily_log_repository_impl import DailyLogRepositoryImpl


class TestDailyLogRepositoryImpl(TestCase):
    @pytest.mark.use_genuine_api()
    def test_fetch_all(self):
        # Given
        # 実際にNotion APIを叩くため、モックではなく本物のLotionを使う
        suite = DailyLogRepositoryImpl(client=Lotion.get_instance(), logger=Mock(spec=Logger))
        date_ = date(2024, 4, 12)

        # When
        daily_log = suite.find(date=date_)

        # Then
        self.assertIsNotNone(daily_log)
