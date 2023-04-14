import pytest

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


@pytest.fixture
def actor_with_single_follower():
    return UserFactory()


@pytest.fixture
def follower(actor_with_single_follower):
    follower = UserFactory()
    actor_with_single_follower.add_friend(follower)
    return follower


def test_create_break_and_invitations_creates_break_and_invites_addressees_which_are_following_the_actor(
    actor, actor_friends, non_following_user
):
    """When a break is created, only the friends of the actor should be invited."""
    addressee_ids = list(map(lambda user: user.uuid, actor_friends))
    addressee_ids.append(non_following_user.uuid)

    break_ = create_break_and_invitation(actor, starting_at=time_from_now(hours=1), addressees=addressee_ids)
    break_invitation = break_.invitation.single()

    actual_addressees = break_invitation.addressees.all()
    expected_addressees = actor.friends.all()

    assert len(actual_addressees) == len(expected_addressees)
    assert all(a in actual_addressees for a in expected_addressees)
    assert non_following_user not in actual_addressees


def test_create_and_invite_followers_to_a_break_creates_break_and_invites_all_the_actors_followers(
    actor, actor_friends, non_following_user
):
    """When a break is created without specifying addressees, all of the actors followers should be invited."""
    break_ = create_break_and_invitation(actor, starting_at=time_from_now(hours=1))
    break_invitation = break_.invitation.single()

    actual_addressees = break_invitation.addressees.all()
    expected_addressees = actor.followed_by.all()

    assert len(actual_addressees) == len(expected_addressees)
    assert all(a in actual_addressees for a in expected_addressees)
    assert non_following_user not in actual_addressees


def test_create_break_and_invitation_creates_break_and_invitation(
    actor_with_single_follower, follower
):
    """Should create a break and corresponding invitation."""
    break_ = create_break_and_invitation(
        actor_with_single_follower, starting_at=time_from_now(hours=1), addressees=[follower.uuid]
    )

    assert break_
    assert break_.invitation.single()


def test_create_break_creates_break_with_correct_connections(
    actor_with_single_follower, follower
):
    """Creating a break should connect the actor to its participants."""
    break_ = create_break_and_invitation(
        actor_with_single_follower, starting_at=time_from_now(hours=1), addressees=[follower.uuid]
    )

    assert break_
    assert actor_with_single_follower, follower in break_.participants


def test_create_invitation_creates_invitation_with_correct_connections(
    actor_with_single_follower, follower
):
    """Creating an invitation should connect the actor as sender, the break as subject and addressees as such."""
    break_ = create_break_and_invitation(
        actor_with_single_follower, starting_at=time_from_now(hours=1), addressees=[follower.uuid]
    )
    break_invitation = break_.invitation.single()

    assert actor_with_single_follower, follower in break_invitation.sender
    assert follower in break_invitation.addressees
    assert break_ in break_invitation.subject


def test_accept_break_invitation_connects_acceptee_to_acceptees(actor):
    """Should connect the actor to the invitations acceptees and the breaks participants."""
    break_invitation = BreakInvitationFactory()
    break_invitation.subject.connect(BreakFactory())
    break_invitation.addressees.connect(actor)

    actual_invitation = accept_break_invitation(actor, break_invitation)
    actual_break = actual_invitation.get_subject()

    assert actor in actual_invitation.acceptees
    assert actor in actual_break.participants


def test_decline_break_invitation_connects_declinee_to_declinees(actor):
    """Should connect the actor to the invitations declinees."""
    break_invitation = BreakInvitationFactory()
    break_invitation.subject.connect(BreakFactory())
    break_invitation.addressees.connect(actor)

    actual_invitation = decline_break_invitation(actor, break_invitation)
    actual_break = actual_invitation.get_subject()

    assert actor in actual_invitation.declinees
    assert actor not in actual_break.participants
