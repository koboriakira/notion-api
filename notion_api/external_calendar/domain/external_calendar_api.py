from abc import ABCMeta, abstractmethod
from datetime import date

from .event import Events


class ExternalCalendarAPI(metaclass=ABCMeta):
    @abstractmethod
    def fetch(self, date_: date) -> Events:
        pass
