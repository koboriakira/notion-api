from dataclasses import dataclass
from datetime import datetime

from util.datetime import jst_now

from .event_category import EventCategory


@dataclass
class Event:
    category: EventCategory
    start: datetime
    end: datetime
    title: str
    detail: str | None = None
    description: str | None = None


@dataclass
class Events:
    value: list[Event]

    def excludes_past_events(self) -> "Events":
        now = jst_now().timestamp()
        return Events([event for event in self.value if event.end.timestamp() >= now])
