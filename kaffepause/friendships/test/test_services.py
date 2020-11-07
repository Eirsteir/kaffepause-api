import pytest

from kaffepause.friendships.exceptions import InvalidFriendshipDeletion
from kaffepause.friendships.models import Friendship, FriendshipStatus
from kaffepause.friendships.services import (
    _attempt_to_delete_blocked_friendship,
    _get_or_create_friendship,
    create_friendship,
    delete_friendship,
)
from kaffepause.friendships.test.factories import FriendshipFactory
from kaffepause.users.test.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_create_friendships(requested_status):
    """Should create and return the created friendship with a default status of 'requested'."""
    from_user = UserFactory()
    to_user = UserFactory()

    friendships = create_friendship(from_user, to_user)

    assert friendships.from_user == from_user
    assert friendships.to_user == to_user
    assert friendships.status == requested_status


def test_create_friendships_with_are_friends_status(are_friends_status):
    """Should create and return the created friendship with the given status."""
    from_user = UserFactory()
    to_user = UserFactory()

    actual_friendships = create_friendship(
        from_user, to_user, status=are_friends_status
    )

    assert actual_friendships.from_user == from_user
    assert actual_friendships.to_user == to_user
    assert actual_friendships.status == are_friends_status


def test_create_friendships_when_friendships_already_exist(
    friendships, requested_status
):
    """Should return the existing friendship."""
    from_user = friendships.from_user
    to_user = friendships.to_user

    actual_friendships = create_friendship(from_user, to_user)

    assert actual_friendships == friendships


def test_create_friendships_when_the_reversed_friendships_already_exist(
    friendships, requested_status
):
    """Should create and return the existing friendship."""
    from_user = friendships.from_user
    to_user = friendships.to_user

    actual_friendships = create_friendship(
        from_user=to_user, to_user=from_user
    )

    assert actual_friendships == friendships


def test_get_or_create_friendships(requested_status):
    """Should create a new friendship with the given users and status when the friendship does not exist."""
    actual_friendships, created = _get_or_create_friendship(
        from_user=UserFactory(), to_user=UserFactory(), status=requested_status
    )

    assert actual_friendships.status == requested_status
    assert created


def test_get_or_create_friendships_when_friendships_exists(friendships):
    """Should return the existing friendship."""
    from_user = friendships.from_user
    to_user = friendships.to_user
    status = friendships.status

    actual_friendships, created = _get_or_create_friendship(
        from_user, to_user, status
    )

    assert actual_friendships == friendships
    assert not created


def test_get_or_create_friendships_when_friendships_exists_with_different_status(
    friendships, are_friends_status
):
    """Should return the existing friendship."""
    from_user = friendships.from_user
    to_user = friendships.to_user

    actual_friendships, created = _get_or_create_friendship(
        from_user, to_user, are_friends_status
    )

    assert actual_friendships == friendships
    assert not created


def test_get_or_create_friendships_when_reverse_friendships_exists(
    friendships,
):
    """Should return the existing friendship."""
    from_user = friendships.to_user
    to_user = friendships.from_user
    status = friendships.status

    actual_friendships, created = _get_or_create_friendship(
        from_user, to_user, status
    )

    assert actual_friendships == friendships
    assert not created


def test_attempt_to_delete_blocked_friendships(blocked_status):
    """Should delete the friendship when the actor is the one blocking."""
    actor = UserFactory()
    friendships = FriendshipFactory(from_user=actor, status=blocked_status)

    _attempt_to_delete_blocked_friendship(actor, friendships)


def test_attempt_to_delete_blocked_friendships_when_actor_is_being_blocked(
    blocked_status,
):
    """Should not delete the friendship when the actor is the one being blocked."""
    actor = UserFactory()
    friendships = FriendshipFactory(to_user=actor, status=blocked_status)

    with pytest.raises(InvalidFriendshipDeletion):
        _attempt_to_delete_blocked_friendship(actor, friendships)


def test_attempt_to_delete_blocked_friendships_when_friendships_status_is_not_blocked(
    requested_status,
):
    """Should not delete the friendship when the status is not 'blocked'."""
    actor = UserFactory()
    friendships = FriendshipFactory(to_user=actor, status=requested_status)

    with pytest.raises(InvalidFriendshipDeletion):
        _attempt_to_delete_blocked_friendship(actor, friendships)


def test_delete_friendships_when_status_is_requested(requested_status):
    """Should delete the friendship when status is 'requested'."""
    actor = UserFactory()
    user = UserFactory()
    friendships = FriendshipFactory(
        from_user=actor, to_user=user, status=requested_status
    )

    delete_friendship(actor, user)

    assert not Friendship.objects.filter(pk=friendships.pk).exists()


def test_delete_friendships_when_status_is_are_friends(are_friends_status):
    """Should delete the friendship when status is 'are_friends'."""
    actor = UserFactory()
    user = UserFactory()
    friendships = FriendshipFactory(
        from_user=actor, to_user=user, status=are_friends_status
    )

    delete_friendship(actor, user)

    assert not Friendship.objects.filter(pk=friendships.pk).exists()


def test_delete_friendships_when_status_is_blocked_and_actor_is_blocking(
    blocked_status,
):
    """Should delete the friendship when status is 'blocked' and the actor is the blocker."""
    actor = UserFactory()
    user = UserFactory()
    friendships = FriendshipFactory(
        from_user=actor, to_user=user, status=blocked_status
    )

    delete_friendship(actor, user)

    assert not Friendship.objects.filter(pk=friendships.pk).exists()


def test_delete_friendships_when_status_is_blocked_and_actor_is_being_blocked(
    blocked_status,
):
    """Should not delete the friendship when status is 'blocked' and the actor is being blocked."""
    actor = UserFactory()
    user = UserFactory()
    FriendshipFactory(from_user=user, to_user=actor, status=blocked_status)

    with pytest.raises(InvalidFriendshipDeletion):
        delete_friendship(actor, user)


def test_both_users_can_delete_the_friendships_when_status_is_valid(
    are_friends_status,
):
    """Both users should be able to delete the friendship when status is not 'blocked'"""
    actor = UserFactory()
    user = UserFactory()
    friendships = FriendshipFactory(
        from_user=actor, to_user=user, status=are_friends_status
    )

    delete_friendship(actor, user)

    assert not Friendship.objects.filter(pk=friendships.pk).exists()

    friendships = FriendshipFactory(
        from_user=actor, to_user=user, status=are_friends_status
    )

    delete_friendship(actor=user, user=actor)

    assert not Friendship.objects.filter(pk=friendships.pk).exists()
