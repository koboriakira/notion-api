from datetime import date, datetime

from notion_client_wrapper.properties.date import Date


class LastEditedTime(Date):
    @staticmethod
    def create(name: str|None = None, value: date|datetime|None = None) -> "LastEditedTime":
        name = name or "最終更新日時"
        return LastEditedTime.from_start_date(name=name, start_date=value)
