from datetime import date, datetime

from notion_client_wrapper.properties.date import Date


class CreatedTime(Date):
    @staticmethod
    def create(value: date|datetime) -> "CreatedTime":
        return CreatedTime.from_start_date(name="作成日時", start_date=value)
