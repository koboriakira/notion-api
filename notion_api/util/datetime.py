from datetime import date, datetime, timedelta, timezone

JST = timezone(timedelta(hours=+9), "JST")

def jst_now() -> datetime:
    return datetime.now(JST)

def jst_today_datetime() -> datetime:
    return jst_now().replace(hour=0, minute=0, second=0, microsecond=0)

def jst_today() -> date:
    return jst_now().date()
