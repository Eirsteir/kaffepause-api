from datetime import datetime
from typing import Callable

from kaffepause.breaks.models import Break, BreakInvitation
from kaffepause.users.models import User


def create_and_invite_friends_to_a_break(
    actor: User, start_time: datetime = None
) -> Break:
    raise NotImplementedError


def _invite_friends_to_break(actor: User, subject: Break) -> None:
    """Create an invitation to given break to all friends of the actor."""
    raise NotImplementedError


def accept_break_invitation(
    actor: User, invitation: BreakInvitation
) -> BreakInvitation:
    __reply_to_invitation(actor, invitation, invitation.accept_on_behalf_of)
    invitation.subject.participants.connect(actor)
    return invitation


def decline_break_invitation(
    actor: User, invitation: BreakInvitation
) -> BreakInvitation:

    return __reply_to_invitation(actor, invitation, invitation.decline_on_behalf_of)


def __reply_to_invitation(
    actor: User, invitation: BreakInvitation, reply_action: Callable
) -> BreakInvitation:
    invitation.ready_for_reply(actor)
    reply_action(actor)

    return invitation
