import pytest

from kaffepause.relationships.test.graphql_requests import SEND_FRIEND_REQUEST_MUTATION
from kaffepause.users.test.factories import UserFactory

pytestmark = pytest.mark.django_db


def get_request_data():
    friend = UserFactory()
    variables = {"toFriend": friend.uid}
    return friend, variables


def test_send_friend_requests_when_can_send_request_sends_request(
    client_query, auth_headers, user
):
    """Should send a friend request to the user when users are not already friends."""
    friend, variables = get_request_data()

    client_query(
        SEND_FRIEND_REQUEST_MUTATION, variables=variables, headers=auth_headers
    )

    assert user.outgoing_friend_requests.is_connected(friend)
    assert friend.incoming_friend_requests.is_connected(user)


def test_send_friend_requests_when_can_send_request_returns_the_user(
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


def test_send_friend_requests_when_already_friends_does_not_send_request(
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


def test_send_friend_requests_when_an_outgoing_request_is_already_sent(
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


def test_send_friend_requests_when_an_incoming_request_is_already_sent(
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


def test_send_friend_requests_when_unauthenticated_fails(snapshot, client_query):
    """A user should not be able to send a friend request when unauthenticated."""
    friend, variables = get_request_data()
    response = client_query(SEND_FRIEND_REQUEST_MUTATION, variables=variables)
    content = response.json()

    snapshot.assert_match(content)
