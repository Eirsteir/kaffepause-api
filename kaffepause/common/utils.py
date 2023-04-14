from datetime import datetime, timedelta

from django.utils import timezone
from django.utils.translation import gettext as _
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


def format_kicker_message(time):
    time_str = format_time_from_now(time)
    return _("Om %(time)s") % {"time": time_str}


def format_time_from_now(target_time) -> str:
    # Calculate the difference between the target time and the current time
    time_diff = target_time - timezone.now()
    # Extract the number of hours and minutes from the time difference
    hours = int(time_diff.total_seconds() // 3600)
    minutes = int((time_diff.total_seconds() % 3600) // 60)
    # Format the result based on the number of hours and minutes
    if hours > 0:
        result = _("%(hours)d timer og %(minutes)d minutter") % {"hours": hours, "minutes": minutes}
    else:
        result = _("%(minutes)d minutter") % {"minutes": minutes}

    return result


def time_from_now(hours=0, minutes=0):
    """Returns the time from now. If now plus given time is in the past, it wraps around to the next day."""
    now = timezone.now()
    start = now + timedelta(hours=hours, minutes=minutes)
    return start if start > now else start + timedelta(days=1)


def jwt_payload(user, context=None):
    payload = graphql_jwt_payload(user, context)
    payload["user_id"] = str(user.id)
    return payload
