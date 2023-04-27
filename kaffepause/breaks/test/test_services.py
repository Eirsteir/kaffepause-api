import pytest

from kaffepause.breaks.exceptions import InvalidBreakStartTime
from kaffepause.breaks.services import (
    accept_break_invitation,
    create_break_and_invitation,
    decline_break_invitation,
)
from kaffepause.breaks.test.factories import BreakFactory, BreakInvitationFactory
from kaffepause.common.utils import time_from_now
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
def non_following_user():
    return UserFactory()


def test_create_break_and_invitation_creates_break_and_invitation(
    actor
):
    """Should create a break and corresponding invitation."""
    break_ = create_break_and_invitation(
        actor, starting_at=time_from_now(hours=1)
    )

    assert break_
    assert break_.invitation.single()


def test_create_break_without_location_creates_break(actor):
    """Should create a break without a location"""
    break_ = create_break_and_invitation(
        actor, starting_at=time_from_now(hours=1)
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
        actor, starting_at=time_from_now(hours=1)
    )
    invitation = break_.invitation.single()
    actual_addressees = invitation.addressees.all()

    assert len(actual_addressees) == 0


def test_create_break_with_addressees_sends_invitation_to_all_addressees(actor, actor_friends):
    """All addressees should be sent an invitation to the break."""
    expected_addressees = list(map(lambda friend: friend.id, actor_friends))
    break_ = create_break_and_invitation(
        actor, starting_at=time_from_now(hours=1), addressees=expected_addressees
    )
    invitation = break_.invitation.single()
    actual_addressees = invitation.addressees.all()

    assert all(a in expected_addressees for a in actual_addressees)


def test_create_break_with_addressees_only_sends_invitation_to_actors_friends(actor, actor_friends):
    """Only friends of the actor should be invited to the break."""
    non_friend = UserFactory()
    addressees = list(map(lambda friend: friend.id, actor_friends)) + [non_friend]

    break_ = create_break_and_invitation(
        actor, starting_at=time_from_now(hours=1), addressees=addressees
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

