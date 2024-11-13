from datetime import date

from external_calendar.domain.event import Event
from external_calendar.domain.external_calendar_api import ExternalCalendarAPI


class ExternalCalendarService:
    def __init__(self, api: ExternalCalendarAPI) -> None:
        self._api = api

    def get_events(self, date_: date) -> list[Event]:
        return self._api.fetch(date_)
