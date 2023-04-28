import uuid

import pytest

from kaffepause.breaks.exceptions import InvalidBreakStartTime, MissingTimeOrLocationInChangeRequestException, \
    InvalidChangeRequestRequestedTime, InvalidChangeRequestForExpiredBreak, BreakNotFound
from kaffepause.breaks.services import (
    accept_break_invitation,
    create_break_and_invitation,
    decline_break_invitation, request_change,
)
from kaffepause.breaks.test.factories import BreakFactory, BreakInvitationFactory
from kaffepause.common.utils import time_from_now

ONE_HOUR_FROM_NOW = time_from_now(hours=1)
from kaffepause.location.tests.factories import LocationFactory
from kaffepause.users.test.factories import UserFactory

pytestmark = pytest.mark.django_db


@pytest.fixture
def actor():
    return UserFactory()


@pytest.fixture
def actor_friends(actor):
    friends = UserFactory.create_batch(10)
    for user in friends:
        actor.add_friend(user)
    return friends


@pytest.fixture
def break_():
    return BreakFactory()


@pytest.fixture
def invitation(actor, break_):
    invitation = BreakInvitationFactory()
    break_.invitation.connect(invitation)
    invitation.addressees.connect(actor)


@pytest.fixture
def location():
    return LocationFactory()



def test_create_break_and_invitation_creates_break_and_invitation(
    actor
):
    """Should create a break and corresponding invitation."""
    break_ = create_break_and_invitation(
        actor, starting_at=ONE_HOUR_FROM_NOW
    )

    assert break_
    assert break_.invitation.single()


def test_create_break_without_location_creates_break(actor):
    """Should create a break without a location"""
    break_ = create_break_and_invitation(
        actor, starting_at=ONE_HOUR_FROM_NOW
    )

    assert break_
    assert not break_.location.single()


def test_create_break_without_start_time_fails(actor):
    """Should fail to create a break without a start time"""
    with pytest.raises(InvalidBreakStartTime):
        create_break_and_invitation(
            actor, starting_at=None
        )


def test_create_break_without_addressees_does_not_invite_anybody(actor):
    """Should create a break and invitation without any addressees."""
    break_ = create_break_and_invitation(
        actor, starting_at=ONE_HOUR_FROM_NOW
    )
    invitation = break_.invitation.single()
    actual_addressees = invitation.addressees.all()

    assert len(actual_addressees) == 0


def test_create_break_with_addressees_sends_invitation_to_all_addressees(actor, actor_friends):
    """All addressees should be sent an invitation to the break."""
    expected_addressees = list(map(lambda friend: friend.id, actor_friends))
    break_ = create_break_and_invitation(
        actor, starting_at=ONE_HOUR_FROM_NOW, addressees=expected_addressees
    )
    invitation = break_.invitation.single()
    actual_addressees = invitation.addressees.all()

    assert all(a in expected_addressees for a in actual_addressees)


def test_create_break_with_addressees_only_sends_invitation_to_actors_friends(actor, actor_friends):
    """Only friends of the actor should be invited to the break."""
    non_friend = UserFactory()
    addressees = list(map(lambda friend: friend.id, actor_friends)) + [non_friend]

    break_ = create_break_and_invitation(
        actor, starting_at=ONE_HOUR_FROM_NOW, addressees=addressees
    )
    invitation = break_.invitation.single()
    actual_addressees = invitation.addressees.all()

    assert non_friend not in actual_addressees


def test_accept_break_invitation_connects_acceptee_to_acceptees(actor):
    """Should connect the actor to the invitations acceptees and the breaks participants."""
    break_invitation = BreakInvitationFactory()
    break_invitation.subject.connect(BreakFactory())
    break_invitation.addressees.connect(actor)

    actual_invitation = accept_break_invitation(actor, break_invitation)
    actual_break = actual_invitation.get_subject()

    assert actor in actual_invitation.confirmed
    assert actor in actual_break.participants


def test_decline_break_invitation_connects_declinee_to_declinees(actor):
    """Should connect the actor to the invitations declinees."""
    break_invitation = BreakInvitationFactory()
    break_invitation.subject.connect(BreakFactory())
    break_invitation.addressees.connect(actor)

    actual_invitation = decline_break_invitation(actor, break_invitation)
    actual_break = actual_invitation.get_subject()

    assert actor in actual_invitation.decliners
    assert actor not in actual_break.participants


def test_request_change_without_time_and_location_fails(actor, break_):
    """Should not be able to request a change without new time or location."""
    with pytest.raises(MissingTimeOrLocationInChangeRequestException):
        request_change(actor=actor, break_uuid=break_.uuid, requested_time=None, requested_location_uuid=None)


def test_request_change_with_new_time_in_past_fails(actor, break_, location):
    """Should not be able to request a change with new time in the past. """
    with pytest.raises(InvalidChangeRequestRequestedTime):
        request_change(actor=actor, break_uuid=break_.uuid, requested_time=time_from_now(hours=-1), requested_location_uuid=location.uuid)


def test_request_change_with_new_time_when_break_is_expired_fails(actor, break_, location):
    """Should not be able to request a change for an expired break."""
    break_.start_time = time_from_now(hours=-1)
    assert break_.is_expired

    with pytest.raises(InvalidChangeRequestForExpiredBreak):
        request_change(actor=actor, break_uuid=break_.uuid, requested_time=ONE_HOUR_FROM_NOW, requested_location_uuid=location.uuid)


def test_request_change_when_break_does_not_exist_fails(actor, location):
    """Should not be able to request change for a non-existing break."""
    with pytest.raises(BreakNotFound):
        request_change(actor=actor, break_uuid=uuid.UUID(), requested_time=ONE_HOUR_FROM_NOW, requested_location_uuid=location.uuid)


def test_request_change_when_actor_is_not_invited_participator_or_initator_fails(break_, location):
    """Should not be able to request change when the actor is not invited, a participator or initiator."""
    with pytest.raises(BreakNotFound):
        request_change(actor=UserFactory(), break_uuid=break_.uuid, requested_time=ONE_HOUR_FROM_NOW, requested_location_uuid=location.uuid)


def test_request_change_when_actor_is_invited_creates_change_request(actor, break_, location):
    """Should not be able to request change when the actor is not invited."""
    actual_break = request_change(actor=actor, break_uuid=break_.uuid, requested_time=ONE_HOUR_FROM_NOW, requested_location_uuid=location.uuid)
    change_request = actual_break.change_requests.first_or_none()
    assert change_request


def test_request_change_when_actor_is_initiator_creates_change_request(actor, break_, invitation, location):
    """Should be able to request change when the actor is initiator."""
    break_.initiator.connect(actor)
    invitation.addressees.disconnect(actor)

    actual_break = request_change(actor=actor, break_uuid=break_.uuid, requested_time=ONE_HOUR_FROM_NOW,
                                  requested_location_uuid=location.uuid)
    change_request = actual_break.change_requests.first_or_none()

    assert change_request


def test_request_change_when_actor_is_participant_creates_change_request(actor, break_, invitation, location):
    """Should be able to request change when the actor is participant."""
    break_.participants.connect(actor)
    invitation.addressees.disconnect(actor)

    actual_break = request_change(actor=actor, break_uuid=break_.uuid, requested_time=ONE_HOUR_FROM_NOW,
                                  requested_location_uuid=location.uuid)
    change_request = actual_break.change_requests.first_or_none()

    assert change_request


def test_request_change_connects_requested_by_to_actor(actor, break_, location):
    """Should connect actor to the change requests requested_by."""
    actual_break = request_change(actor=actor, break_uuid=break_.uuid, requested_time=ONE_HOUR_FROM_NOW,
                                  requested_location_uuid=location.uuid)
    change_request = actual_break.change_requests.first_or_none()

    assert actor == change_request.requested_by.single()


def test_request_change_connects_requested_for_to_break_(actor, break_, location):
    """Should connect break to the change requests requested_for."""
    actual_break = request_change(actor=actor, break_uuid=break_.uuid, requested_time=ONE_HOUR_FROM_NOW,
                                  requested_location_uuid=location.uuid)
    change_request = actual_break.change_requests.first_or_none()

    assert break_ == change_request.requested_for.single()


def test_request_change_connects_requested_location_to_location(actor, break_, location):
    """Should connect location to the change requests requested_location."""
    actual_break = request_change(actor=actor, break_uuid=break_.uuid, requested_time=ONE_HOUR_FROM_NOW,
                                  requested_location_uuid=location.uuid)
    change_request = actual_break.change_requests.first_or_none()

    assert location == change_request.requested_location.single()


def test_request_change_sets_requested_time(actor, break_):
    """Should save the change request with the requested time."""
    actual_break = request_change(actor=actor, break_uuid=break_.uuid, requested_time=ONE_HOUR_FROM_NOW)
    change_request = actual_break.change_requests.first_or_none()

    assert ONE_HOUR_FROM_NOW == change_request.requested_time
