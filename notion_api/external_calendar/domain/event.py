from dataclasses import dataclass
from datetime import datetime

from .event_category import EventCategory


@dataclass
class Event:
    category: EventCategory
    start: datetime
    end: datetime
    title: str
    detail: str | None = None
    description: str | None = None
