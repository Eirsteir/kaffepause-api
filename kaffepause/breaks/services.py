from datetime import datetime
from typing import Callable, List

from kaffepause.breaks.models import Break, BreakInvitation
from kaffepause.users.models import User


def create_break_and_invitation(
    actor: User, addressees: List[int], start_time: datetime = None
) -> Break:
    """
    Create a break and an invitation to given addressees, optionally at the given start time.
    Will not send an invitation to addressees which are not following the actor.
    """
    follower_selection = actor.followed_by.filter(uid__in=addressees)
    return _create_break_and_invitation(actor, follower_selection, start_time)


def create_break_and_invite_followers(
    actor: User, start_time: datetime = None
) -> Break:
    """Create a break and an invitation all of the users followers, optionally at the given start time."""
    followers = actor.followed_by.all()
    return _create_break_and_invitation(actor, followers, start_time)


def _create_break_and_invitation(
    actor: User, followers: List[User], start_time: datetime = None
) -> Break:
    break_ = _create_break(actor, start_time)
    _create_invitation(actor, break_, followers)
    return break_


def _create_break(actor: User, start_time: datetime) -> Break:
    """Create break with given start time and connect actor to its participants."""
    break_ = Break(start_time=start_time).save()
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
    __reply_to_invitation(actor, invitation, invitation.accept_on_behalf_of)
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
