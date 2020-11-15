from datetime import datetime, timedelta


def get_first_matching_attr(obj, *attrs, default=None):
    for attr in attrs:
        if hasattr(obj, attr):
            return getattr(obj, attr)

    return default


def thirty_minutes_from_now():
    now = datetime.now()
    start = now + timedelta(minutes=30)
    return start if start > now else start + timedelta(days=1)


def three_hours_from_now():
    now = datetime.now()
    start = now + timedelta(hours=3)
    return start if start > now else start + timedelta(days=1)
