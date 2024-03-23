from datetime import date, datetime, timedelta, timezone

JST = timezone(timedelta(hours=+9), "JST")

def jst_now() -> datetime:
    return datetime.now(JST)

def jst_today_datetime() -> datetime:
    return jst_now().replace(hour=0, minute=0, second=0, microsecond=0)

def jst_today() -> date:
    return jst_now().date()

def convert_to_date_or_datetime(value: str|None, cls: type|None = None) -> date | datetime | None:
    if value is None:
        return None
    length_date = 10 # "YYYY-MM-DD"
    value_error_msg = f"Invalid class: {cls}"
    if len(value) == length_date:
        tmp_date = date.fromisoformat(value)
        if cls is None or cls == date:
            return tmp_date
        if cls == datetime:
            return datetime(tmp_date.year, tmp_date.month, tmp_date.day, tzinfo=JST)
        raise ValueError(value_error_msg)
    tmp_datetime = datetime.fromisoformat(value)
    if cls is None or cls == datetime:
        return tmp_datetime
    if cls == date:
        return tmp_datetime.date()
    raise ValueError(value_error_msg)
