import pytest

from kaffepause.accounts.test.factories import AccountFactory
from kaffepause.friendships.exceptions import (
    InvalidFriendshipDeletion,
    UnnecessaryStatusUpdate,
)
from kaffepause.friendships.models import Friendship
from kaffepause.friendships.services import (
    __update_friendship_status,
    _attempt_to_delete_blocked_friendship,
    _get_or_create_friendship,
    accept_friend_request,
    create_friendship,
    delete_friendship,
)
from kaffepause.friendships.test.factories import FriendshipFactory

pytestmark = pytest.mark.django_db


def test_create_friendships(requested_status):
    """Should create and return the created friendship with a default status of 'requested'."""
    from_user = AccountFactory()
    to_user = AccountFactory()

    friendships = create_friendship(from_user, to_user)

    assert friendships.from_user == from_user
    assert friendships.to_user == to_user
    assert friendships.status == requested_status


def test_create_friendships_with_are_friends_status(are_friends_status):
    """Should create and return the created friendship with the given status."""
    from_user = AccountFactory()
    to_user = AccountFactory()

    actual_friendships = create_friendship(
        from_user, to_user, status=are_friends_status
    )

    assert actual_friendships.from_user == from_user
    assert actual_friendships.to_user == to_user
    assert actual_friendships.status == are_friends_status


def test_create_friendships_when_friendships_already_exist(
    friendship, requested_status
):
    """Should return the existing friendship."""
    from_user = friendship.from_user
    to_user = friendship.to_user

    actual_friendships = create_friendship(from_user, to_user)

    assert actual_friendships == friendship


def test_create_friendships_when_the_reversed_friendships_already_exist(
    friendship, requested_status
):
    """Should create and return the existing friendship."""
    from_user = friendship.from_user
    to_user = friendship.to_user

    actual_friendships = create_friendship(from_user=to_user, to_user=from_user)

    assert actual_friendships == friendship


def test_get_or_create_friendships(requested_status):
    """Should create a new friendship with the given users and status when the friendship does not exist."""
    actual_friendships, created = _get_or_create_friendship(
        from_user=AccountFactory(), to_user=AccountFactory(), status=requested_status
    )

    assert actual_friendships.status == requested_status
    assert created


def test_get_or_create_friendships_when_friendships_exists(friendship):
    """Should return the existing friendship."""
    from_user = friendship.from_user
    to_user = friendship.to_user
    status = friendship.status

    actual_friendships, created = _get_or_create_friendship(from_user, to_user, status)

    assert actual_friendships == friendship
    assert not created


def test_get_or_create_friendships_when_friendships_exists_with_different_status(
    friendship, are_friends_status
):
    """Should return the existing friendship."""
    from_user = friendship.from_user
    to_user = friendship.to_user

    actual_friendships, created = _get_or_create_friendship(
        from_user, to_user, are_friends_status
    )

    assert actual_friendships == friendship
    assert not created


def test_get_or_create_friendships_when_reverse_friendships_exists(
    friendship,
):
    """Should return the existing friendship."""
    from_user = friendship.to_user
    to_user = friendship.from_user
    status = friendship.status

    actual_friendships, created = _get_or_create_friendship(from_user, to_user, status)

    assert actual_friendships == friendship
    assert not created


def test_attempt_to_delete_blocked_friendships(blocked_status):
    """Should delete the friendship when the actor is the one blocking."""
    actor = AccountFactory()
    friendships = FriendshipFactory(from_user=actor, status=blocked_status)

    _attempt_to_delete_blocked_friendship(actor, friendships)


def test_attempt_to_delete_blocked_friendships_when_actor_is_being_blocked(
    blocked_status,
):
    """Should not delete the friendship when the actor is the one being blocked."""
    actor = AccountFactory()
    friendships = FriendshipFactory(to_user=actor, status=blocked_status)

    with pytest.raises(InvalidFriendshipDeletion):
        _attempt_to_delete_blocked_friendship(actor, friendships)


def test_attempt_to_delete_blocked_friendships_when_friendships_status_is_not_blocked(
    requested_status,
):
    """Should not delete the friendship when the status is not 'blocked'."""
    actor = AccountFactory()
    friendships = FriendshipFactory(to_user=actor, status=requested_status)

    with pytest.raises(InvalidFriendshipDeletion):
        _attempt_to_delete_blocked_friendship(actor, friendships)


def test_delete_friendships_when_status_is_requested(requested_status):
    """Should delete the friendship when status is 'requested'."""
    actor = AccountFactory()
    user = AccountFactory()
    friendships = FriendshipFactory(
        from_user=actor, to_user=user, status=requested_status
    )

    delete_friendship(actor, user)

    assert not Friendship.objects.filter(pk=friendships.pk).exists()


def test_delete_friendships_when_status_is_are_friends(are_friends_status):
    """Should delete the friendship when status is 'are_friends'."""
    actor = AccountFactory()
    user = AccountFactory()
    friendships = FriendshipFactory(
        from_user=actor, to_user=user, status=are_friends_status
    )

    delete_friendship(actor, user)

    assert not Friendship.objects.filter(pk=friendships.pk).exists()


def test_delete_friendships_when_status_is_blocked_and_actor_is_blocking(
    blocked_status,
):
    """Should delete the friendship when status is 'blocked' and the actor is the blocker."""
    actor = AccountFactory()
    user = AccountFactory()
    friendships = FriendshipFactory(
        from_user=actor, to_user=user, status=blocked_status
    )

    delete_friendship(actor, user)

    assert not Friendship.objects.filter(pk=friendships.pk).exists()


def test_delete_friendships_when_status_is_blocked_and_actor_is_being_blocked(
    blocked_status,
):
    """Should not delete the friendship when status is 'blocked' and the actor is being blocked."""
    actor = AccountFactory()
    user = AccountFactory()
    FriendshipFactory(from_user=user, to_user=actor, status=blocked_status)

    with pytest.raises(InvalidFriendshipDeletion):
        delete_friendship(actor, user)


def test_both_users_can_delete_the_friendships_when_status_is_valid(
    are_friends_status,
):
    """Both users should be able to delete the friendship when status is not 'blocked'"""
    actor = AccountFactory()
    user = AccountFactory()
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


def test_update_friendship_status_updates_to_new_status(
    requested_status, are_friends_status
):
    """Should update the friendship to the new status."""
    from_user = AccountFactory()
    to_user = AccountFactory()
    old_status = requested_status
    new_status = are_friends_status

    FriendshipFactory(from_user=from_user, to_user=to_user, status=old_status)

    friendship = __update_friendship_status(from_user, to_user, old_status, new_status)

    assert friendship.status == new_status


def test_update_friendship_status_when_attempting_to_update_to_same_status(
    requested_status, are_friends_status
):
    """Should update the friendship to the new status."""
    from_user = AccountFactory()
    to_user = AccountFactory()
    old_status = requested_status
    new_status = requested_status

    FriendshipFactory(from_user=from_user, to_user=to_user, status=old_status)

    with pytest.raises(UnnecessaryStatusUpdate):
        __update_friendship_status(from_user, to_user, old_status, new_status)


def test_accept_friend_request(requested_status, are_friends_status):
    """Should update the status to 'are_friends' when the update request is valid."""
    from_user = AccountFactory()
    to_user = AccountFactory()
    old_status = requested_status
    new_status = are_friends_status

    FriendshipFactory(from_user=from_user, to_user=to_user, status=old_status)

    friendship = accept_friend_request(actor=to_user, from_user=from_user)

    assert friendship.status == new_status


def test_accept_friend_request_when_existing_friendship_is_not_requested(
    are_friends_status,
):
    """Should update the status to 'are_friends' when the update request is valid."""
    from_user = AccountFactory()
    to_user = AccountFactory()

    FriendshipFactory(from_user=from_user, to_user=to_user, status=are_friends_status)

    with pytest.raises(Friendship.DoesNotExist):
        accept_friend_request(actor=to_user, from_user=from_user)


def test_only_user_to_which_the_friendship_is_incoming_to_can_accept_friend_request(
    requested_status, are_friends_status
):
    """Should update the status to 'are_friends' when the update request is valid."""
    from_user = AccountFactory()
    to_user = AccountFactory()

    FriendshipFactory(from_user=from_user, to_user=to_user, status=requested_status)

    with pytest.raises(Friendship.DoesNotExist):
        accept_friend_request(actor=from_user, from_user=to_user)
