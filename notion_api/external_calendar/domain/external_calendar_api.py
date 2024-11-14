from abc import ABCMeta, abstractmethod
from datetime import date

from .event import Event


class ExternalCalendarAPI(metaclass=ABCMeta):
    @abstractmethod
    def fetch(self, date: date, excludes_past_events: bool | None = None) -> list[Event]:
        pass
