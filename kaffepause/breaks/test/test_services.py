import pytest

from kaffepause.breaks.services import (
    create_break_and_invitation,
    create_break_and_invite_followers,
)
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
    """When a break is created, only the friends following the actor should be invited."""
    addressee_ids = list(map(lambda user: user.uid, actor_friends))
    addressee_ids.append(non_following_user.uid)

    break_ = create_break_and_invitation(actor, addressee_ids)
    break_invitation = break_.invitation.single()

    actual_addressees = break_invitation.addressees.all()
    expected_addressees = actor.followed_by.all()

    assert len(actual_addressees) == len(expected_addressees)
    assert all(a in actual_addressees for a in expected_addressees)
    assert non_following_user not in actual_addressees


def test_create_and_invite_followers_to_a_break_creates_break_and_invites_all_the_actors_followers(
    actor, actor_friends, non_following_user
):
    """When a break is created without specifying addressees, all of the actors followers should be invited."""
    break_ = create_break_and_invite_followers(actor)
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
        actor_with_single_follower, addressees=[follower.uid]
    )

    assert break_
    assert break_.invitation.single()


def test_create_break_creates_break_with_correct_connections(
    actor_with_single_follower, follower
):
    """Creating a break should connect the actor to its participants."""
    break_ = create_break_and_invitation(
        actor_with_single_follower, addressees=[follower.uid]
    )

    assert break_
    assert actor_with_single_follower, follower in break_.participants


def test_create_invitation_creates_invitation_with_correct_connections(
    actor_with_single_follower, follower
):
    """Creating an invitation should connect the actor as sender, the break as subject and addressees as such."""
    break_ = create_break_and_invitation(
        actor_with_single_follower, addressees=[follower.uid]
    )
    break_invitation = break_.invitation.single()

    assert actor_with_single_follower, follower in break_invitation.sender
    assert follower in break_invitation.addressees
    assert break_ in break_invitation.subject
