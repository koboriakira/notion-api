from datetime import date

from external_calendar.domain.event import Events
from external_calendar.domain.external_calendar_api import ExternalCalendarAPI


class ExternalCalendarService:
    def __init__(self, api: ExternalCalendarAPI) -> None:
        self._api = api

    def get_events(self, date_: date, excludes_past_events: bool | None = None) -> Events:
        events = self._api.fetch(date_=date_)
        if excludes_past_events:
            events = events.excludes_past_events()
        return events
