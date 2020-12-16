from datetime import datetime
from typing import Callable, List

from kaffepause.breaks.models import Break, BreakInvitation
from kaffepause.users.models import User


def create_break_and_invitation(
    actor: User, addressees: List[str] = None, starting_at: datetime = None
) -> Break:
    """
    Create a break and an invitation to given addressees, optionally at the given start time.
    If addressees are specified, only send the invitation to the ones who are following the users.
    If not, send to all followers.
    """
    if addressees:
        addressees = actor.followed_by.filter(uuid__in=addressees)
    else:
        addressees = actor.followed_by.all()

    return _create_break_and_invitation(actor, addressees, starting_at)


def _create_break_and_invitation(
    actor: User, followers: List[User], starting_at: datetime = None
) -> Break:
    break_ = _create_break(actor, starting_at)
    _create_invitation(actor, break_, followers)
    return break_


def _create_break(actor: User, starting_at: datetime) -> Break:
    """Create break with given start time and connect actor to its participants."""
    break_ = Break(starting_at=starting_at).save()
    break_.participants.connect(actor)
    return break_


def _create_invitation(actor: User, break_: Break, addressees: List[User]) -> None:
    """
    Create an invitation for given break and connect the actor as its sender and the break as its subject.
    Will be addressed to all given addressees.
    """
    break_invitation = BreakInvitation().save()
    break_invitation.sender.connect(actor)
    break_invitation.subject.connect(break_)
    for addressee in addressees:
        break_invitation.addressees.connect(addressee)


def accept_break_invitation(
    actor: User, invitation: BreakInvitation
) -> BreakInvitation:
    invitation = __reply_to_invitation(
        actor, invitation, invitation.accept_on_behalf_of
    )
    invitation.get_subject().participants.connect(actor)
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
