from datetime import date, datetime

from notion_client_wrapper.properties.date import Date


class CreatedTime(Date):
    @staticmethod
    def create(name: str|None = None, value: date|datetime|None = None) -> "CreatedTime":
        name = name or "作成日時"
        return CreatedTime.from_start_date(name=name, start_date=value)
