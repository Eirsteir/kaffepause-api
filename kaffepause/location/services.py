import logging

from django.core.exceptions import ValidationError

from kaffepause.location.models import Location
from kaffepause.users.models import User

logger = logging.getLogger(__name__)


def add_user_location(user: User, title: str) -> Location:
    title = title.strip()
    if not title:
        raise ValidationError("Du må legge til et stedsnavn.")

    return Location.get_or_create({"title": title, "item_type": "USER"}, relationship=user.custom_locations)[0]

