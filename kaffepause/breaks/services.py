from django.contrib.auth import get_user_model
from django.utils.timezone import localtime

from kaffepause.breaks.models import Break

User = get_user_model()


def create_and_invite_friends_to_a_break(actor: User, start_time: localtime) -> Break:
    """Create a :class:`Break` and invite the actors friends to it."""
    pass
