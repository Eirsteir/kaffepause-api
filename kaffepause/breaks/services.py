from datetime import datetime
from typing import Callable, List
from uuid import UUID

from django.utils import timezone

from kaffepause.breaks.exceptions import MissingOrIdenticalTimeAndLocationInChangeRequestException, \
    InvalidChangeRequestForExpiredBreak, InvalidChangeRequestRequestedTime
from kaffepause.breaks.models import Break, BreakInvitation, ChangeRequest
from kaffepause.breaks.selectors import get_break
from kaffepause.common.utils import time_from_now
from kaffepause.notifications.enums import NotificationEntityType
from kaffepause.notifications.services import bulk_notify, notify
from kaffepause.users.models import User
from kaffepause.location.models import Location
from kaffepause.location.selectors import get_location_or_none


def create_break_and_invitation(
    actor: User, starting_at: datetime, addressees: List = None, location: str = None
) -> Break:
    """
    Create a break and an invitation to given addressees, optionally at the given location.
    Only invite the actors actual friends.
    """
    if addressees:
        addressees = actor.friends.filter(uuid__in=addressees)
    else:
        addressees = []

    location = get_location_or_none(location_uuid=location)

    break_ = _create_break_and_invitation(actor, addressees, starting_at, location)

    bulk_notify(
        notifiers=addressees,
        entity_type=NotificationEntityType.BREAK_INVITATION_SENT,
        entity_id=break_.uuid,
        actor=actor,
        entity_potential_start_time=starting_at,
        location_name=location.title if location else None,
        starting_at=timezone.localtime(starting_at).strftime("%H:%M"))

    return break_


def _create_break_and_invitation(
    actor: User, followers: List[User], starting_at: datetime = None, location: Location = None
) -> Break:
    break_ = _create_break(actor, starting_at, location)
    if followers:
        _create_invitation(actor, break_, followers)
    return break_


def _create_break(actor: User, starting_at: datetime, location: Location) -> Break:
    """Create break with given start time and connect actor to its participants."""
    break_ = Break(starting_at=starting_at).save()
    break_.participants.connect(actor)
    break_.initiator.connect(actor)
    if location:
        break_.location.connect(location)
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
    __notify_invitation_reply(invitation=invitation, actor=actor, entity_type=NotificationEntityType.BREAK_INVITATION_ACCEPTED)
    return invitation


def decline_break_invitation(
    actor: User, invitation: BreakInvitation
) -> BreakInvitation:

    invitation = __reply_to_invitation(actor, invitation, invitation.decline_on_behalf_of)
    __notify_invitation_reply(invitation=invitation, actor=actor,
                              entity_type=NotificationEntityType.BREAK_INVITATION_DECLINED)
    return invitation


def ignore_break_invitation(
    actor: User, invitation: BreakInvitation
) -> BreakInvitation:

    return __reply_to_invitation(actor, invitation, invitation.ignore_on_behalf_of)


def __reply_to_invitation(
    actor: User, invitation: BreakInvitation, reply_action: Callable
) -> BreakInvitation:
    invitation.ready_for_reply(actor)
    reply_action(actor)

    return invitation


def __notify_invitation_reply(invitation: BreakInvitation, actor: User, entity_type: NotificationEntityType):
    notify(
        user=invitation.get_sender(),
        entity_type=entity_type,
        entity_id=invitation.get_subject().uuid,
        actor=actor
    )


def request_change(
    *, actor: User, break_uuid: UUID, requested_time: datetime = None, requested_location_uuid: UUID = None
) -> ChangeRequest:
    break_ = get_break(actor=actor, uuid=break_uuid)

    if break_.is_expired:
        raise InvalidChangeRequestForExpiredBreak

    if requested_location_uuid and requested_location_uuid == break_.location.single().uuid:
        requested_location_uuid = None

    if requested_time == break_.starting_at:
        requested_time = None

    if not requested_time and not requested_location_uuid:
        raise MissingOrIdenticalTimeAndLocationInChangeRequestException

    if requested_time and requested_time <= time_from_now(minutes=5):  # TODO: setting
        raise InvalidChangeRequestRequestedTime

    change_request = ChangeRequest(requested_time=requested_time).save()
    change_request.requested_by.connect(actor)
    change_request.requested_for.connect(break_)

    if requested_location_uuid:
        requested_location = get_location_or_none(location_uuid=requested_location_uuid)
        change_request.requested_location.connect(requested_location)

    return break_
