import pytest

from kaffepause.relationships.test.graphql_requests import (
    CANCEL_FRIEND_REQUEST_MUTATION,
    SEND_FRIEND_REQUEST_MUTATION,
)
from kaffepause.users.test.factories import UserFactory

pytestmark = pytest.mark.django_db


@pytest.fixture
def requested_friend(user):
    friend = UserFactory()
    user.send_friend_request(friend)
    return friend


def get_request_data():
    friend = UserFactory()
    variables = {"toFriend": friend.uid}
    return friend, variables


def test_send_friend_request_when_can_send_request_sends_request(
    client_query, auth_headers, user
):
    """Should send a friend request to the user when users are not already friends."""
    friend, variables = get_request_data()

    client_query(
        SEND_FRIEND_REQUEST_MUTATION, variables=variables, headers=auth_headers
    )

    assert user.outgoing_friend_requests.is_connected(friend)
    assert friend.incoming_friend_requests.is_connected(user)


def test_send_friend_request_when_can_send_request_returns_the_user(
    client_query, auth_headers
):
    """Should return the recipient of the request."""
    friend, variables = get_request_data()
    response = client_query(
        SEND_FRIEND_REQUEST_MUTATION, variables=variables, headers=auth_headers
    )

    content = response.json()
    data = content.get("data").get("sendFriendRequest")

    assert data.get("sentFriendRequestee").get("uuid") == friend.uid
    assert data.get("success")
    assert not data.get("errors")


def test_send_friend_request_when_already_friends_does_not_send_request(
    snapshot, client_query, auth_headers, user
):
    """Should not send a friend request to the user when users are already friends."""
    friend, variables = get_request_data()
    user.friends.connect(friend)

    response = client_query(
        SEND_FRIEND_REQUEST_MUTATION, variables=variables, headers=auth_headers
    )
    content = response.json()

    snapshot.assert_match(content)


def test_send_friend_request_when_an_outgoing_request_is_already_sent(
    snapshot, client_query, auth_headers, user
):
    """Should not send a friend request to the user if a friendship is already requested."""
    friend, variables = get_request_data()
    user.outgoing_friend_requests.connect(friend)

    response = client_query(
        SEND_FRIEND_REQUEST_MUTATION, variables=variables, headers=auth_headers
    )
    content = response.json()

    snapshot.assert_match(content)


def test_send_friend_request_when_an_incoming_request_is_already_sent(
    snapshot, client_query, auth_headers, user
):
    """Should not send a friend request to the user if a friendship is already requested."""
    friend, variables = get_request_data()
    user.incoming_friend_requests.connect(friend)

    response = client_query(
        SEND_FRIEND_REQUEST_MUTATION, variables=variables, headers=auth_headers
    )
    content = response.json()

    snapshot.assert_match(content)


def test_send_friend_request_when_unauthenticated_fails(snapshot, client_query):
    """A user should not be able to send a friend request when unauthenticated."""
    friend, variables = get_request_data()
    response = client_query(SEND_FRIEND_REQUEST_MUTATION, variables=variables)
    content = response.json()

    snapshot.assert_match(content)


def test_cancel_friend_request_when_can_cancel_request_cancels_request(
    client_query, auth_headers, requested_friend, user
):
    """Should cancel a friend request to the user when a request has been sent by the user."""

    variables = {"toFriend": requested_friend.uid}
    client_query(
        CANCEL_FRIEND_REQUEST_MUTATION, variables=variables, headers=auth_headers
    )

    assert not user.outgoing_friend_requests.is_connected(requested_friend)
    assert not requested_friend.incoming_friend_requests.is_connected(user)


def test_cancel_friend_request_when_can_cancel_request_returns_the_user(
    client_query, auth_headers
):
    """Should return the recipient of the request."""
    friend, variables = get_request_data()
    response = client_query(
        CANCEL_FRIEND_REQUEST_MUTATION, variables=variables, headers=auth_headers
    )

    content = response.json()
    data = content.get("data").get("cancelFriendRequest")

    assert data.get("cancelledFriendRequestee").get("uuid") == friend.uid
    assert data.get("success")
    assert not data.get("errors")


def test_cancel_friend_requests_when_already_friends_does_nothing(
    snapshot, client_query, auth_headers, requested_friend, user
):
    """Should do nothing when the users are already friends."""
    user.add_friend(requested_friend)
    variables = {"toFriend": requested_friend.uid}

    response = client_query(
        CANCEL_FRIEND_REQUEST_MUTATION, variables=variables, headers=auth_headers
    )
    content = response.json()

    snapshot.assert_match(content)


def test_cancel_friend_requests_when_addressee_attempts_to_cancel(
    snapshot, client_query, auth_headers, requested_friend, user
):
    """Should do nothing when the users are already friends."""
    user.add_friend(requested_friend)
    variables = {"toFriend": str(user.uid)}

    response = client_query(
        CANCEL_FRIEND_REQUEST_MUTATION, variables=variables, headers=auth_headers
    )
    content = response.json()

    snapshot.assert_match(content)


def test_cancel_friend_requests_when_unauthenticated_fails(snapshot, client_query):
    """A user should not be able to cancel a friend request when unauthenticated."""
    friend, variables = get_request_data()
    response = client_query(CANCEL_FRIEND_REQUEST_MUTATION, variables=variables)
    content = response.json()

    snapshot.assert_match(content)
