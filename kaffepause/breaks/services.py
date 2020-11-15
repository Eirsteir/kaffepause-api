from datetime import datetime
from typing import Callable

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from kaffepause.breaks.exceptions import InvalidInvitationUpdate
from kaffepause.breaks.models import Break, BreakInvitation
from kaffepause.friendships.selectors import get_friends

User = get_user_model()


def create_and_invite_friends_to_a_break(
    actor: User, start_time: datetime = None
) -> Break:
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


def accept_break_invitation(
    actor: User, invitation: BreakInvitation
) -> BreakInvitation:
    return __reply_to_invitation(actor, invitation, invitation.accept)


def decline_break_invitation(
    actor: User, invitation: BreakInvitation
) -> BreakInvitation:
    return __reply_to_invitation(actor, invitation, invitation.decline)


def ignore_break_invitation(
    actor: User, invitation: BreakInvitation
) -> BreakInvitation:
    return __reply_to_invitation(actor, invitation, invitation.ignore)


def __reply_to_invitation(
    actor: User, invitation: BreakInvitation, action: Callable
) -> BreakInvitation:
    if actor != invitation.recipient:
        raise InvalidInvitationUpdate(_("Invitation does not belong to this user"))

    action()

    return invitation
