from datetime import datetime, timedelta


def get_first_matching_attr(obj, *attrs, default=None):
    for attr in attrs:
        if hasattr(obj, attr):
            return getattr(obj, attr)

    return default


def thirty_minutes_from_now():
    return time_from_now(minutes=30)


def three_hours_from_now():
    return time_from_now(hours=3)


def time_from_now(hours=0, minutes=0):
    now = datetime.now()
    start = now + timedelta(hours=hours, minutes=minutes)
    return start if start > now else start + timedelta(days=1)
