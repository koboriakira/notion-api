from datetime import datetime
from unittest import TestCase

from external_calendar.domain.event import Event
from external_calendar.domain.event_category import EventCategory
from external_calendar.domain.event_converter import EventConverter


class TestEventConverter(TestCase):
    def test_convert_to_domain(self):
        # Given
        event = {
            "category": "プライベート",
            "start": "2024-11-13T18:30:00+09:00",
            "end": "2024-11-13T21:30:00+09:00",
            "title": "さんかく屋根のお家へようこそ！vol.2 (19:30開始)",
            "detail": None,
            "description": '<a href="https://t.livepocket.jp/myticket/index">https://t.livepocket.jp/myticket/index</a>',
        }
        # When
        actual = EventConverter.to_object(event)

        # Then
        expected = Event(
            category=EventCategory.PRIVATE,
            start=datetime.fromisoformat("2024-11-13T18:30:00+09:00"),
            end=datetime.fromisoformat("2024-11-13T21:30:00+09:00"),
            title="さんかく屋根のお家へようこそ！vol.2 (19:30開始)",
            detail=None,
            description='<a href="https://t.livepocket.jp/myticket/index">https://t.livepocket.jp/myticket/index</a>',
        )
        self.assertEqual(actual, expected)
