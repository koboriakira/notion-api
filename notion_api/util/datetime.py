from datetime import date, datetime, timedelta, timezone
from enum import Enum

JST = timezone(timedelta(hours=+9), "JST")

LENGTH_DATE = 10  # "YYYY-MM-DD"


class DateType(Enum):
    DATE = "date"
    DATETIME = "datetime"
    NONE = "none"

    @staticmethod
    def get_datetype(value: date | datetime | None) -> "DateType":
        if value is None:
            return DateType.NONE
        try:
            # それぞれ変換できることを確認してから返却する
            if len(value) == LENGTH_DATE:
                date.fromisoformat(value)
                return DateType.DATE
            datetime.fromisoformat(value)
            return DateType.DATETIME
        except ValueError:
            return DateType.NONE


def jst_now() -> datetime:
    return datetime.now(JST)


def jst_today_datetime() -> datetime:
    return jst_now().replace(hour=0, minute=0, second=0, microsecond=0)


def jst_today() -> date:
    return jst_now().date()


def convert_to_date_or_datetime(value: str | None, cls: type | None = None) -> date | datetime | None:
    date_type = DateType.get_datetype(value)
    match date_type:
        case DateType.DATE:
            tmp_date = date.fromisoformat(value)
            return datetime(tmp_date.year, tmp_date.month, tmp_date.day, tzinfo=JST) if cls == datetime else tmp_date
        case DateType.DATETIME:
            tmp_datetime = datetime.fromisoformat(value)
            return (
                tmp_datetime.date()
                if cls == date or (tmp_datetime.hour == 0 and tmp_datetime.minute == 0)
                else tmp_datetime
            )
        case DateType.NONE:
            return None
