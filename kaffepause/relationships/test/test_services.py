import pytest
from neomodel import clear_neo4j_database, db

from kaffepause.relationships.exceptions import (
    CannotAcceptFriendRequest,
    RelationshipAlreadyExists,
)
from kaffepause.relationships.services import (
    accept_friend_request,
    cancel_friend_request,
    send_friend_request,
)
from kaffepause.users.test.factories import UserFactory

pytestmark = pytest.mark.django_db

# https://github.com/hspandher/django-test-addons#testing-neo4j-graph-database


@pytest.fixture(autouse=True)
def setup_and_teardown():
    clear_neo4j_database(db)
    yield
    clear_neo4j_database(db)


def test_send_friend_request():
    """Should create a 'REQUESTED' relationship between the users."""
    actor = UserFactory().save()
    addressee = UserFactory().save()

    send_friend_request(actor, addressee)

    assert actor in addressee.incoming_friend_requests
    assert addressee in actor.outgoing_friend_requests


def test_send_friend_request_when_users_have_a_connection():
    """Relationship should not be created if a relationship between the users already exists"""
    actor = UserFactory().save()
    addressee = UserFactory().save()

    actor.friends.connect(addressee)

    with pytest.raises(RelationshipAlreadyExists):
        send_friend_request(actor, addressee)


def test_send_friend_request_when_users_are_blocked():
    """Should deny any action when one of the users has blocked the other."""
    pass


def test_cancel_friend_request():
    """Should delete a 'REQUESTED_FRIEND' relationship between the users."""
    actor = UserFactory().save()
    addressee = UserFactory().save()
    send_friend_request(actor, addressee)

    cancel_friend_request(actor, addressee)

    assert not addressee.incoming_friend_requests.get_or_none(uid=actor.uid)
    assert not actor.outgoing_friend_requests.get_or_none(uid=addressee.uid)


def test_cancel_friend_request_when_no_request_exists():
    """Should delete a 'REQUESTED_FRIEND' relationship between the users if no such request exists."""
    actor = UserFactory().save()
    addressee = UserFactory().save()

    cancel_friend_request(actor, addressee)

    assert not addressee.incoming_friend_requests.get_or_none(uid=actor.uid)
    assert not actor.outgoing_friend_requests.get_or_none(uid=addressee.uid)


def test_accept_friend_request():
    """
    Should create an 'ARE_FRIENDS' relationship between the users
    if a 'REQUESTED_FRIEND' relationship exists from actor to the other.
    """
    actor = UserFactory().save()
    requester = UserFactory().save()

    send_friend_request(actor=requester, to_user=actor)

    accept_friend_request(actor, requester)

    assert actor.friends.get_or_none(uid=requester.uid)
    assert not actor.incoming_friend_requests.get_or_none(uid=requester.uid)
    assert not requester.outgoing_friend_requests.get_or_none(uid=actor.uid)


def test_accept_friend_request_without_a_request_having_been_sent():
    """A user should not be able to accept a friend request if none has been sent."""
    actor = UserFactory().save()
    from_user = UserFactory().save()

    with pytest.raises(CannotAcceptFriendRequest):
        accept_friend_request(actor, from_user)


def test_accept_friend_request_when_already_friends():
    """Should return successfully when the users are already friends."""
    actor = UserFactory().save()
    requester = UserFactory().save()

    actor.friends.connect(requester)

    accept_friend_request(actor, requester)

    assert actor.friends.get_or_none(uid=requester.uid)
    assert not actor.incoming_friend_requests.get_or_none(uid=requester.uid)
    assert not requester.outgoing_friend_requests.get_or_none(uid=actor.uid)
