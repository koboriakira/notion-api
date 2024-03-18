from datetime import date, datetime

from notion_client_wrapper.properties.date import Date


class LastEditedTime(Date):
    @staticmethod
    def create(value: date|datetime) -> "LastEditedTime":
        return LastEditedTime.from_start_date(name="最終更新日時", start_date=value)
