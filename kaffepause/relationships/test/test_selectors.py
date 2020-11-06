import pytest

from kaffepause.relationships.selectors import get_friendships
from kaffepause.relationships.test.factories import RelationshipFactory

pytestmark = pytest.mark.django_db


def test_get_friends_of(user, are_friends_status, requested_status):
    """Should return exclusively users who are in an accepted friendship relation with the given user."""
    outgoing_accepted = RelationshipFactory(from_user=user, status=are_friends_status)
    incoming_accepted = RelationshipFactory(to_user=user, status=are_friends_status)
    RelationshipFactory(to_user=user, status=requested_status)

    friends = get_friendships(user, are_friends_status)

    assert friends.count() == 2
    assert friends.filter(id=outgoing_accepted.to_user.id).exists()
    assert friends.filter(id=incoming_accepted.from_user.id).exists()


# def test_get_friends_of_when_user_has_no_friends(user):
#     """Should return no users."""
#     friends = get_friends_of(user)
#
#     assert not friends.count()
#
#
# def test_get_incoming_requests_for(user):
#     """Should return all users who have sent a friend request to the given user."""
#     incoming_request = FriendshipFactory(
#         addressee=user, status=FriendshipStatus.REQUESTED
#     )
#
#     FriendshipFactory.create(requester=user, status=FriendshipStatus.REQUESTED)
#     FriendshipFactory.create(addressee=user, status=FriendshipStatus.ACCEPTED)
#     FriendshipFactory.create(requester=user, status=FriendshipStatus.BLOCKED)
#
#     friends = get_incoming_friend_requests_for(user)
#
#     print(user)
#     print(user.friends.all())
#     print(friends.all())
#     print(incoming_request.requester)
#     print(Friendship.objects.all())
#
#     assert friends.count() == 1
#     assert friends.filter(id=incoming_request.requester.id).exists()
