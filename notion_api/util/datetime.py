from datetime import datetime, timedelta, timezone

JST = timezone(timedelta(hours=+9), "JST")

def jst_now():
    return datetime.now(JST)

def jst_today():
    return jst_now().date()
