from datetime import datetime

from django.contrib.auth import get_user_model

from kaffepause.breaks.models import Break, BreakInvitation
from kaffepause.friendships.selectors import get_friends

User = get_user_model()


def create_and_invite_friends_to_a_break(
    actor: User, start_time: datetime = None
) -> Break:
    """Create a :class:`Break` and invite the actors friends to it."""
    subject = Break.objects.create(start_time=start_time)
    subject.add_participant(actor)
    _invite_friends_to_break(actor, subject)
    return subject


def _invite_friends_to_break(actor: User, subject: Break) -> None:
    """Create an invitation to given break to all friends of the actor."""
    friend_ids = get_friends(actor).values_list("id", flat=True)
    invitations = [
        BreakInvitation(sender=actor, recipient_id=friend_id, subject=subject)
        for friend_id in friend_ids
    ]

    BreakInvitation.objects.bulk_create(invitations)
