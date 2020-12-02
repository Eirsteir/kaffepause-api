import pytest

from kaffepause.relationships.enums import NonRelatedRelationship, UserRelationship
from kaffepause.relationships.selectors import (
    get_friendship_status,
    get_mutual_friends_count,
)
from kaffepause.users.test.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_get_mutual_friends_count():
    """Should return the number of mutual friends between the given users."""
    actor = UserFactory()
    user = UserFactory()
    mutual_friend = UserFactory()

    actor.friends.connect(user)
    actor.friends.connect(mutual_friend)

    user.friends.connect(mutual_friend)

    # Make sure others are not included
    actor.friends.connect(UserFactory())
    user.friends.connect(UserFactory())

    mutual_friends_count = get_mutual_friends_count(actor, user)

    assert mutual_friends_count == 1


def test_get_friendship_status_when_friends():
    """Should return the correct relationship type when user are friends."""
    actor = UserFactory()
    user = UserFactory()

    actor.friends.connect(user)

    friendship_status = get_friendship_status(actor, user)

    assert friendship_status == str(UserRelationship.ARE_FRIENDS)


def test_get_friendship_status_when_incoming_request():
    """Should return the correct relationship type when one user has requested the friendship of the actor."""
    actor = UserFactory()
    user = UserFactory()

    actor.incoming_friend_requests.connect(user)

    friendship_status = get_friendship_status(actor, user)

    assert friendship_status == str(UserRelationship.REQUESTING_FRIENDSHIP)


def test_get_friendship_status_when_outgoing_request():
    """Should return the 'CANNOT_REQUEST' relationship type when one actor has requested the friendship of the user."""
    actor = UserFactory()
    user = UserFactory()

    actor.outgoing_friend_requests.connect(user)

    friendship_status = get_friendship_status(actor, user)

    assert friendship_status == str(NonRelatedRelationship.CANNOT_REQUEST)


def test_get_friendship_status_when_not_connected():
    """Should return the defaUlt 'CAN_REQUEST' relationship type when not connected."""
    actor = UserFactory()
    user = UserFactory()

    friendship_status = get_friendship_status(actor, user)

    assert friendship_status == str(NonRelatedRelationship.CAN_REQUEST)


def test_get_friendship_status_when_friend_is_self():
    """Should return None when actor is requesting friendship status to itself."""
    pass
