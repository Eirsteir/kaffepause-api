from datetime import timedelta

from django.utils import timezone


def get_first_matching_attr(obj, *attrs, default=None):
    for attr in attrs:
        if hasattr(obj, attr):
            return getattr(obj, attr)

    return default


def fifteen_minutes_from_now():
    return time_from_now(minutes=30)


def three_hours_from_now():
    return time_from_now(hours=3)


def time_from_now(hours=0, minutes=0):
    now = timezone.now()
    start = now + timedelta(hours=hours, minutes=minutes)
    return start if start > now else start + timedelta(days=1)
