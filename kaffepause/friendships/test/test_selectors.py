import pytest

from kaffepause.friendships.enums import NonFriendsFriendshipStatus
from kaffepause.friendships.models import Friendship
from kaffepause.friendships.selectors import (
    friendship_exists,
    get_friends,
    get_friendship_status,
    get_friendships_for,
    get_incoming_blocks,
    get_incoming_friendships_for,
    get_incoming_requests,
    get_outgoing_blocks,
    get_outgoing_friendships_for,
    get_outgoing_requests,
    get_single_friendship,
)
from kaffepause.friendships.test.factories import FriendshipFactory
from kaffepause.users.test.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_get_friendships_for(user, are_friends_status, requested_status):
    """Should return exclusively users who are in an accepted friendship with the given user."""
    outgoing_accepted = FriendshipFactory(from_user=user, status=are_friends_status)
    incoming_accepted = FriendshipFactory(to_user=user, status=are_friends_status)

    # Leave out other friendship
    FriendshipFactory(to_user=user, status=requested_status)

    friends = get_friendships_for(user, are_friends_status)

    assert friends.count() == 2
    assert friends.filter(id=outgoing_accepted.to_user.id).exists()
    assert friends.filter(id=incoming_accepted.from_user.id).exists()


def test_get_friendships_for_when_user_has_no_friendships(user, are_friends_status):
    """Should return no users when user has no friendship."""
    friends = get_friendships_for(user, are_friends_status)

    assert not friends.count()


def test_get_incoming_friendships_for(
    user, are_friends_status, blocked_status, requested_status
):
    """Should return all users who have created a friendship to the given user."""
    incoming_request = FriendshipFactory(to_user=user, status=requested_status)

    # Leave out other friendship
    FriendshipFactory.create(from_user=user, status=requested_status)
    FriendshipFactory.create(to_user=user, status=are_friends_status)
    FriendshipFactory.create(from_user=user, status=blocked_status)

    friends = get_incoming_friendships_for(user, requested_status)

    assert friends.count() == 1
    assert friends.filter(id=incoming_request.from_user.id).exists()


def test_get_outgoing_friendships_for(
    user, are_friends_status, blocked_status, requested_status
):
    """Should return all users who the given user has created a friendship to."""
    outgoing_request = FriendshipFactory(from_user=user, status=requested_status)

    # Leave out other friendship
    FriendshipFactory.create(to_user=user, status=requested_status)
    FriendshipFactory.create(to_user=user, status=are_friends_status)
    FriendshipFactory.create(from_user=user, status=blocked_status)

    friends = get_outgoing_friendships_for(user, requested_status)

    assert friends.count() == 1
    assert friends.filter(id=outgoing_request.to_user.id).exists()


def test_friendships_exists_excluding_status_asymmetrical(friendship):
    """Should return true if a friendship with the respective users exists."""
    from_user = friendship.from_user
    to_user = friendship.to_user

    assert friendship_exists(from_user, to_user)


def test_friendships_exists_excluding_status_asymmetrical_reversed(
    friendship,
):
    """Should return true if a friendship with the respective users exists."""
    from_user = friendship.to_user
    to_user = friendship.from_user

    assert not friendship_exists(from_user, to_user)


def test_friendships_exists_excluding_status_asymmetrical_when_it_does_not_exist():
    """Should return false if an asymmetrical friendship with the respective users does not exist."""

    assert not friendship_exists(from_user=UserFactory(), to_user=UserFactory())


def test_friendships_exists_including_status_asymmetrical(friendship):
    """Should return true if an asymmetrical friendship with the respective users and status exists."""
    from_user = friendship.from_user
    to_user = friendship.to_user
    status = friendship.status

    assert friendship_exists(from_user, to_user, status)


def test_friendships_exists_including_status_asymmetrical_reversed(
    friendship,
):
    """Should return false if an asymmetrical reversed friendship with the respective users and status does not exists."""
    from_user = friendship.to_user
    to_user = friendship.from_user
    status = friendship.status

    assert not friendship_exists(from_user, to_user, status)


def test_friendships_exists_including_status__asymmetrical_when_it_does_not_exist(
    requested_status,
):
    """Should return false if an asymmetrical friendship with the respective users and status does not exist."""

    assert not friendship_exists(
        from_user=UserFactory(), to_user=UserFactory(), status=requested_status
    )


def test_friendships_exists_excluding_status_symmetrical(friendship):
    """Should return true if a symmetrical friendship with the respective users exists."""
    from_user = friendship.from_user
    to_user = friendship.to_user

    assert friendship_exists(from_user, to_user, symmetrical=True)


def test_friendships_exists_excluding_status_symmetrical_reversed(
    friendship,
):
    """Should return true if a symmetrical friendship with the respective users exists."""
    from_user = friendship.to_user
    to_user = friendship.from_user

    assert friendship_exists(from_user, to_user, symmetrical=True)


def test_friendships_exists_excluding_status_symmetrical_when_it_does_not_exist():
    """Should return false if a symmetrical friendship with the respective users does not exist."""

    assert not friendship_exists(
        from_user=UserFactory(), to_user=UserFactory(), symmetrical=True
    )


def test_friendships_exists_including_status_symmetrical(friendship):
    """Should return true if a symmetrical friendship with the respective users and status exists."""
    from_user = friendship.from_user
    to_user = friendship.to_user
    status = friendship.status

    assert friendship_exists(from_user, to_user, status=status, symmetrical=True)


def test_friendships_exists_including_status_symmetrical_reversed(
    friendship,
):
    """Should return true if a symmetrical friendship with the respective users and status exists."""
    from_user = friendship.from_user
    to_user = friendship.to_user
    status = friendship.status

    assert friendship_exists(from_user, to_user, status=status, symmetrical=True)


def test_friendships_exists_including_status__symmetrical_when_it_does_not_exist(
    requested_status,
):
    """Should return false if a symmetrical friendship with the respective users and status does not exist."""

    assert not friendship_exists(
        from_user=UserFactory(),
        to_user=UserFactory(),
        status=requested_status,
        symmetrical=True,
    )


def test_get_friends(user, are_friends_status, requested_status):
    """Should return exclusively users who are in an accepted friendship with the given user."""
    outgoing_accepted = FriendshipFactory(from_user=user, status=are_friends_status)
    incoming_accepted = FriendshipFactory(to_user=user, status=are_friends_status)

    # Leave out other friendship
    FriendshipFactory(to_user=user, status=requested_status)

    friends = get_friends(user)

    assert friends.count() == 2
    assert friends.filter(id=outgoing_accepted.to_user.id).exists()
    assert friends.filter(id=incoming_accepted.from_user.id).exists()


def test_get_incoming_requests(
    user, are_friends_status, blocked_status, requested_status
):
    """Should return all users who have created a requested friendship to the given user."""
    incoming_request = FriendshipFactory(to_user=user, status=requested_status)

    # Leave out other friendship
    FriendshipFactory.create(from_user=user, status=requested_status)
    FriendshipFactory.create(to_user=user, status=are_friends_status)
    FriendshipFactory.create(from_user=user, status=blocked_status)

    friends = get_incoming_requests(user)

    assert friends.count() == 1
    assert friends.filter(id=incoming_request.from_user.id).exists()


def test_get_outgoing_requests(
    user, are_friends_status, blocked_status, requested_status
):
    """Should return all users who the given user has created a requested friendship to."""
    outgoing_request = FriendshipFactory(from_user=user, status=requested_status)

    # Leave out other friendship
    FriendshipFactory.create(to_user=user, status=requested_status)
    FriendshipFactory.create(to_user=user, status=are_friends_status)
    FriendshipFactory.create(from_user=user, status=blocked_status)

    friends = get_outgoing_requests(user)

    assert friends.count() == 1
    assert friends.filter(id=outgoing_request.to_user.id).exists()


def test_get_incoming_blocks(
    user, are_friends_status, blocked_status, requested_status
):
    """Should return all users who have created a blocked friendship to the given user."""
    incoming_block = FriendshipFactory(to_user=user, status=blocked_status)

    # Leave out other friendship
    FriendshipFactory.create(from_user=user)
    FriendshipFactory.create(to_user=user, status=are_friends_status)
    FriendshipFactory.create(from_user=user)

    friends = get_incoming_blocks(user)

    assert friends.count() == 1
    assert friends.filter(id=incoming_block.from_user.id).exists()


def test_get_outgoing_blocks(
    user, are_friends_status, blocked_status, requested_status
):
    """Should return all users who the given user has created a blocked friendship to."""
    outgoing_block = FriendshipFactory(from_user=user, status=blocked_status)

    # Leave out other friendship
    FriendshipFactory.create(to_user=user, status=requested_status)
    FriendshipFactory.create(to_user=user, status=are_friends_status)
    FriendshipFactory.create(from_user=user, status=are_friends_status)

    friends = get_outgoing_blocks(user)

    assert friends.count() == 1
    assert friends.filter(id=outgoing_block.to_user.id).exists()


def test_get_single_friendships_excluding_status(friendship):
    """Should return the friendship if a friendship with the respective users exists."""
    from_user = friendship.from_user
    to_user = friendship.to_user

    actual_friendships = get_single_friendship(from_user, to_user)

    assert actual_friendships == friendship


def test_get_single_friendships_excluding_status_reversed(
    friendship,
):
    """Should return the friendship if a reversed friendship with the respective users exists."""
    from_user = friendship.to_user
    to_user = friendship.from_user

    actual_friendships = get_single_friendship(from_user, to_user)

    assert actual_friendships == friendship


def test_get_single_friendships_excluding_status_when_it_does_not_exist():
    """Should raise an exception if a friendship with the respective users does not exist."""
    with pytest.raises(Friendship.DoesNotExist):
        get_single_friendship(from_user=UserFactory(), to_user=UserFactory())


def test_get_single_friendships_including_status(friendship):
    """Should return  the friendship if a friendship with the respective users and status exists."""
    from_user = friendship.from_user
    to_user = friendship.to_user
    status = friendship.status

    actual_friendships = get_single_friendship(from_user, to_user, status)

    assert actual_friendships == friendship


def test_get_single_friendships_including_status_reversed(
    friendship,
):
    """Should return nothing if a reversed friendship with the respective users and status does not exists."""
    from_user = friendship.to_user
    to_user = friendship.from_user
    status = friendship.status

    actual_friendships = get_single_friendship(from_user, to_user, status)

    assert actual_friendships == friendship


def test_get_single_friendships_including_status__when_it_does_not_exist(
    requested_status,
):
    """Should raise an exception if a friendship with the respective users and status does not exist."""
    with pytest.raises(Friendship.DoesNotExist):
        get_single_friendship(
            from_user=UserFactory(),
            to_user=UserFactory(),
            status=requested_status,
        )


def test_get_friendship_status(are_friends_status):
    """Should return the friendship status as a :class:`BaseFriendshipStatusEnum`."""
    actor = UserFactory()
    user = UserFactory()
    friendship = FriendshipFactory(
        from_user=actor, to_user=user, status=are_friends_status
    )

    expected_status = friendship.status
    actual_status = get_friendship_status(actor, user)

    assert actual_status.name == expected_status.name


def test_get_friendship_status_when_friendship_does_not_exist(
    are_friends_status,
):
    """Should return the friendship status as 'CAN_REQUEST' of :class:`NonFriendsFriendshipStatus`."""
    actor = UserFactory()
    user = UserFactory()

    expected_status = NonFriendsFriendshipStatus.CAN_REQUEST
    actual_status = get_friendship_status(actor, user)

    assert actual_status.name == expected_status.name
