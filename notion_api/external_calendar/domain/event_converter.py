from datetime import datetime

from .event import Event, Events
from .event_category import EventCategory


class EventConverter:
    @staticmethod
    def to_object(event: dict) -> Event:
        return Event(
            category=EventCategory(event["category"]),
            start=datetime.fromisoformat(event["start"]),
            end=datetime.fromisoformat(event["end"]),
            title=event["title"],
            detail=event.get("detail"),
            description=event.get("description"),
        )

    @staticmethod
    def to_objects(events: list[dict]) -> Events:
        return Events([EventConverter.to_object(event) for event in events])
