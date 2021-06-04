from datetime import timedelta

from django.utils import timezone
from graphql_jwt.utils import jwt_payload as graphql_jwt_payload


def get_first_matching_attr(obj, *attrs, default=None):
    for attr in attrs:
        if hasattr(obj, attr):
            return getattr(obj, attr)

    return default


def fifteen_minutes_from_now():
    return time_from_now(minutes=15)


def three_hours_from_now():
    return time_from_now(hours=3)


def time_from_now(hours=0, minutes=0):
    """Returns the time from now. If now plus given time is in the past, it wraps around to the next day."""
    now = timezone.now()
    start = now + timedelta(hours=hours, minutes=minutes)
    return start if start > now else start + timedelta(days=1)


def jwt_payload(user, context=None):
    payload = graphql_jwt_payload(user, context)
    payload["user_id"] = str(user.id)
    return payload
