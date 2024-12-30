from datetime import date
from unittest import TestCase

from daily_log.isoweek import Isoweek


class TestIsoweek(TestCase):
    def test(self):
        # Given
        date_ = date(2024, 4, 12)

        # When
        actual = Isoweek.of(date_)

        # Then
        self.assertEqual(actual.year, 2024)
        self.assertEqual(actual.isoweeknum, 15)
        self.assertEqual(actual.start_date, date(2024, 4, 8))  # そのISO週の月曜日が最初
        self.assertEqual(actual.end_date, date(2024, 4, 14))  # そのISO週の日曜日が最後
        self.assertEqual(str(actual), "2024-Week15")
        self.assertEqual(
            actual.date_range(),
            [
                date(2024, 4, 8),
                date(2024, 4, 9),
                date(2024, 4, 10),
                date(2024, 4, 11),
                date(2024, 4, 12),
                date(2024, 4, 13),
                date(2024, 4, 14),
            ],
        )
