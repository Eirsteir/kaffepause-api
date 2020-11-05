import pytest

from kaffepause.friendships.enums import FriendshipStatus
from kaffepause.friendships.models import Friendship
from kaffepause.friendships.selectors import (
    get_friends_of,
    get_friendships,
    get_incoming_friend_requests_for,
)
from kaffepause.friendships.test.factories import FriendshipFactory

pytestmark = pytest.mark.django_db


def test_get_friends_of(user):
    """Should return exclusively users who are in an accepted friendship relation with the given user."""
    outgoing_accepted = FriendshipFactory(
        requester=user, status=FriendshipStatus.ACCEPTED
    )
    incoming_accepted = FriendshipFactory(
        addressee=user, status=FriendshipStatus.ACCEPTED
    )

    friends = get_friendships(user, FriendshipStatus.ACCEPTED)

    assert friends.count() == 2
    assert friends.filter(id=outgoing_accepted.addressee.id).exists()
    assert friends.filter(id=incoming_accepted.requester.id).exists()


def test_get_friends_of_when_user_has_no_friends(user):
    """Should return no users."""
    friends = get_friends_of(user)

    assert not friends.count()


def test_get_incoming_requests_for(user):
    """Should return all users who have sent a friend request to the given user."""
    incoming_request = FriendshipFactory(
        addressee=user, status=FriendshipStatus.REQUESTED
    )

    FriendshipFactory.create(requester=user, status=FriendshipStatus.REQUESTED)
    FriendshipFactory.create(addressee=user, status=FriendshipStatus.ACCEPTED)
    FriendshipFactory.create(requester=user, status=FriendshipStatus.BLOCKED)

    friends = get_incoming_friend_requests_for(user)

    print(user)
    print(user.friends.all())
    print(friends.all())
    print(incoming_request.requester)
    print(Friendship.objects.all())

    assert friends.count() == 1
    assert friends.filter(id=incoming_request.requester.id).exists()
