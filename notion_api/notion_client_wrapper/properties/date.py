from dataclasses import dataclass
from datetime import date
from datetime import datetime as DatetimeObject

from notion_client_wrapper.properties.property import Property


@dataclass
class Date(Property):
    start: str | None = None
    end: str | None = None
    time_zone: str | None = None
    type: str = "date"

    def __init__(self, name: str, id: str | None = None, start: str = None, end: str = None, time_zone: str = None):
        self.name = name
        self.id = id
        self.start = start
        self.end = end
        self.time_zone = time_zone

    @staticmethod
    def of(name: str, param: dict) -> "Date":
        if param["date"] is None:
            return Date(name=name, id=param["id"])
        return Date(
            name=name,
            id=param["id"],
            start=param["date"]["start"],
            end=param["date"]["end"],
            time_zone=param["date"]["time_zone"],
        )

    @staticmethod
    def from_start_date(name: str, start_date: date | DatetimeObject | None = None) -> "Date":
        return Date(
            name=name,
            start=start_date.isoformat() if start_date is not None else None,
        )


    @staticmethod
    def from_range(name: str, start: date|DatetimeObject, end: date|DatetimeObject) -> "Date":
        return Date(
            name=name,
            start=start.isoformat(),
            end=end.isoformat(),
        )

    def __dict__(self):
        return {
            self.name: {
                "type": self.type,
                "date": {
                    "start": self.start,
                    "end": self.end,
                    "time_zone": self.time_zone,
                },
            },
        }

    def value_for_filter(self) -> str:
        raise NotImplementedError
