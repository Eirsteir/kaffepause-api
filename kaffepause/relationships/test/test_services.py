import pytest

from kaffepause.relationships.exceptions import (
    CannotAcceptFriendRequest,
    CannotCancelFriendRequest,
    CannotFollowUser,
    CannotRejectFriendRequest,
    CannotUnfollowUser,
    RelationshipAlreadyExists,
)
from kaffepause.relationships.services import (
    accept_friend_request,
    cancel_friend_request,
    follow_friend,
    reject_friend_request,
    send_friend_request,
    unfollow_friend,
    unfriend_user,
)
from kaffepause.users.test.factories import UserFactory

pytestmark = pytest.mark.django_db


@pytest.fixture
def actor():
    return UserFactory()


@pytest.fixture
def requester():
    return UserFactory()


@pytest.fixture
def addressee():
    return UserFactory()


def test_send_friend_request(actor, addressee):
    """Should create a 'REQUESTED' relationship between the users."""
    send_friend_request(actor, addressee)

    assert actor in addressee.incoming_friend_requests
    assert addressee in actor.outgoing_friend_requests


def test_send_friend_request_when_users_have_a_connection(actor, addressee):
    """Relationship should not be created if a relationship between the users already exists"""
    actor.friends.connect(addressee)

    with pytest.raises(RelationshipAlreadyExists):
        send_friend_request(actor, addressee)


def test_send_friend_request_when_users_are_blocked():
    """Should deny any action when one of the users has blocked the other."""
    pass


def test_cancel_friend_request(actor, addressee):
    """Should delete a 'REQUESTED_FRIEND' relationship between the users."""
    send_friend_request(actor, addressee)

    cancel_friend_request(actor, addressee)

    assert not addressee.incoming_friend_requests.get_or_none(uuid=actor.uuid)
    assert not actor.outgoing_friend_requests.get_or_none(uuid=addressee.uuid)


def test_cancel_friend_request_when_no_request_exists(actor, addressee):
    """Should delete a 'REQUESTED_FRIEND' relationship between the users if no such request exists."""
    cancel_friend_request(actor, addressee)

    assert not addressee.incoming_friend_requests.get_or_none(uuid=actor.uuid)
    assert not actor.outgoing_friend_requests.get_or_none(uuid=addressee.uuid)


def test_cancel_friend_request_when_users_are_already_friends_raises_exception(
    actor, addressee
):
    """Should raise an exception if the user attempts to cancel a friend request when the users are already friends."""
    actor.add_friend(addressee)
    with pytest.raises(CannotCancelFriendRequest):
        cancel_friend_request(actor, addressee)


def test_cancel_friend_request_when_actor_is_addressee_raises_exception(
    actor, addressee
):
    """Should raise an exception if the user attempts to cancel a friend request to itself."""

    with pytest.raises(CannotCancelFriendRequest):
        cancel_friend_request(actor, actor)


def test_accept_friend_request(actor, requester):
    """
    Should create an 'ARE_FRIENDS' relationship between the users
    if a 'REQUESTED_FRIEND' relationship exists from one to the other.
    """
    send_friend_request(actor=requester, to_user=actor)

    accept_friend_request(actor, requester)

    assert actor.friends.get_or_none(uuid=requester.uuid)
    assert not actor.incoming_friend_requests.get_or_none(uuid=requester.uuid)
    assert not requester.outgoing_friend_requests.get_or_none(uuid=actor.uuid)


def test_accept_friend_request_makes_users_follow_each_other(actor, requester):
    """
    Friends should follow each other when a friendship is initiated.
    """
    send_friend_request(actor=requester, to_user=actor)

    accept_friend_request(actor, requester)

    assert actor.following.get_or_none(uuid=requester.uuid)
    assert requester.following.get_or_none(uuid=actor.uuid)

    assert actor.followed_by.get_or_none(uuid=requester.uuid)
    assert requester.followed_by.get_or_none(uuid=actor.uuid)


def test_only_addressee_can_accept_friend_request(actor, requester):
    """The requester of a friend request should not be able to also accept it."""
    send_friend_request(actor=requester, to_user=actor)

    with pytest.raises(CannotAcceptFriendRequest):
        accept_friend_request(actor=requester, requester=actor)


def test_accept_friend_request_without_a_request_having_been_sent(actor, requester):
    """A user should not be able to accept a friend request if none has been sent."""

    with pytest.raises(CannotAcceptFriendRequest):
        accept_friend_request(actor, requester)


def test_accept_friend_request_when_already_friends(actor, requester):
    """Should return successfully when the users are already friends."""
    actor.friends.connect(requester)

    accept_friend_request(actor, requester)

    assert actor.friends.get_or_none(uuid=requester.uuid)
    assert not actor.incoming_friend_requests.get_or_none(uuid=requester.uuid)
    assert not requester.outgoing_friend_requests.get_or_none(uuid=actor.uuid)


def test_reject_friend_request(actor, requester):
    """
    Should disconnect the 'REQUESTED_FRIEND' relationship between the users
    if such exists from actor to the other.
    """
    send_friend_request(actor=requester, to_user=actor)

    reject_friend_request(actor, requester)

    assert not actor.friends.get_or_none(uuid=requester.uuid)
    assert not actor.incoming_friend_requests.get_or_none(uuid=requester.uuid)
    assert not requester.outgoing_friend_requests.get_or_none(uuid=actor.uuid)


def test_only_addressee_can_reject_friend_request(actor, requester):
    """Only the addressee of a friend request should be able to reject it."""
    send_friend_request(actor=requester, to_user=actor)

    with pytest.raises(CannotRejectFriendRequest):
        reject_friend_request(actor=requester, requester=actor)


def test_reject_friend_request_without_a_request_having_been_sent(actor, requester):
    """A user should not be able to reject a friend request if none has been sent."""

    with pytest.raises(CannotRejectFriendRequest):
        reject_friend_request(actor, requester)


def test_reject_friend_request_when_already_friends(actor, requester):
    """Should return successfully when the users are already friends."""
    actor.friends.connect(requester)
    accept_friend_request(actor, requester)

    assert actor.friends.get_or_none(uuid=requester.uuid)
    assert not actor.incoming_friend_requests.get_or_none(uuid=requester.uuid)
    assert not requester.outgoing_friend_requests.get_or_none(uuid=actor.uuid)


def test_remove_friend(actor, addressee):
    actor.add_friend(addressee)
    unfriend_user(actor, addressee)

    assert not actor.friends.relationship(addressee)
    assert not actor.incoming_friend_requests.relationship(addressee)
    assert not actor.outgoing_friend_requests.relationship(addressee)


def test_follow_friend_when_friends_and_not_following_follows_the_friend(actor, user):
    """Should make the actor follow the user when they are friends."""
    actor.add_friend(user)
    actor.unfollow_user(user)

    follow_friend(actor=actor, friend=user)

    assert actor.friends.is_connected(user)
    assert actor.following.is_connected(user)
    assert user.following.is_connected(actor)


def test_follow_friend_when_friends_and_already_following_follows_the_friend(
    actor, user
):
    """The actor should still be following the user when attempting to follow one it has already followed."""
    actor.add_friend(user)

    follow_friend(actor=actor, friend=user)

    assert actor.friends.is_connected(user)
    assert actor.following.is_connected(user)
    assert user.following.is_connected(actor)


def test_follow_friend_when_not_friends_fails(actor, user):
    """Should raise an exception if the user attempts to follow a non-friend."""
    with pytest.raises(CannotFollowUser):
        follow_friend(actor=actor, friend=user)


def test_follow_friend_when_attempting_to_follow_self_fails(actor, user):
    """Should raise an exception if the actor attempts to follow itself."""
    with pytest.raises(CannotFollowUser):
        follow_friend(actor=actor, friend=actor)


def test_unfollow_friend_when_friends_unfollows_the_friend(actor, user):
    """Should remove the user from the actors following list but keep the friend connection."""
    actor.add_friend(user)

    unfollow_friend(actor=actor, friend=user)

    assert actor.friends.is_connected(user)
    assert not actor.following.is_connected(user)
    assert user.following.is_connected(actor)


def test_unfollow_friend_when_friends_but_not_following_does_nothing(actor, user):
    """The actor should still be not following the user when attempting to unfollow one it has already unfollowed."""
    actor.add_friend(user)
    actor.unfollow_user(user)

    unfollow_friend(actor=actor, friend=user)

    assert actor.friends.is_connected(user)
    assert not actor.following.is_connected(user)
    assert user.following.is_connected(actor)


def test_unfollow_friend_when_not_friends_fails(actor, user):
    """Should raise an exception if the user attempts to unfollow a non-friend."""
    with pytest.raises(CannotUnfollowUser):
        unfollow_friend(actor=actor, friend=user)


def test_unfollow_friend_when_actor_is_user_fails(actor):
    """Should raise an exception if the user attempts to unfollow itself."""
    with pytest.raises(CannotUnfollowUser):
        unfollow_friend(actor=actor, friend=actor)
