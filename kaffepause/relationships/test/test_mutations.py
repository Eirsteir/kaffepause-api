from types import SimpleNamespace

import pytest

from kaffepause.accounts.models import Account
from kaffepause.relationships.test.graphql_requests import (
    ACCEPT_FRIEND_REQUEST_MUTATION,
    CANCEL_FRIEND_REQUEST_MUTATION,
    FOLLOW_FRIEND_MUTATION,
    SEND_FRIEND_REQUEST_MUTATION,
    UNFOLLOW_FRIEND_MUTATION,
    UNFRIEND_USER_MUTATION,
)
from kaffepause.users.test.factories import UserFactory

pytestmark = pytest.mark.django_db


@pytest.fixture
def requested_friend(user):
    friend = UserFactory()
    user.send_friend_request(friend)
    return friend


@pytest.fixture
def requesting_friend(user):
    friend = UserFactory()
    friend.send_friend_request(user)
    return friend


@pytest.fixture
def friend(user):
    friend = UserFactory()
    user.add_friend(friend)
    return friend


def get_request_data():
    friend = UserFactory()
    variables = {"toFriend": friend.uuid}
    return friend, variables


def test_send_friend_request_when_can_send_request_sends_request(
    client_query, auth_headers, user
):
    """Should send a friend request to the user when users are not already friends."""
    friend, variables = get_request_data()

    client_query(
        SEND_FRIEND_REQUEST_MUTATION,
        op_name="sendFriendRequest",
        variables=variables,
        headers=auth_headers,
    )

    assert user.outgoing_friend_requests.is_connected(friend)
    assert friend.incoming_friend_requests.is_connected(user)


def test_send_friend_request_when_can_send_request_returns_the_user(
    client_query, auth_headers
):
    """Should return the recipient of the request."""
    friend, variables = get_request_data()
    response = client_query(
        SEND_FRIEND_REQUEST_MUTATION,
        op_name="sendFriendRequest",
        variables=variables,
        headers=auth_headers,
    )

    content = response.json()
    data = content.get("data").get("sendFriendRequest")

    assert data.get("sentFriendRequestee").get("uuid") == friend.uuid
    assert data.get("success")
    assert not data.get("errors")


def test_send_friend_request_when_already_friends_does_not_send_request(
    snapshot, client_query, auth_headers, user
):
    """Should not send a friend request to the user when users are already friends."""
    friend, variables = get_request_data()
    user.friends.connect(friend)

    response = client_query(
        SEND_FRIEND_REQUEST_MUTATION,
        op_name="sendFriendRequest",
        variables=variables,
        headers=auth_headers,
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
        SEND_FRIEND_REQUEST_MUTATION,
        op_name="sendFriendRequest",
        variables=variables,
        headers=auth_headers,
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
        SEND_FRIEND_REQUEST_MUTATION,
        op_name="sendFriendRequest",
        variables=variables,
        headers=auth_headers,
    )
    content = response.json()

    snapshot.assert_match(content)


def test_send_friend_request_when_unauthenticated_fails(snapshot, client_query):
    """A user should not be able to send a friend request when unauthenticated."""
    friend, variables = get_request_data()
    response = client_query(
        SEND_FRIEND_REQUEST_MUTATION, op_name="sendFriendRequest", variables=variables
    )
    content = response.json()

    snapshot.assert_match(content)


def test_cancel_friend_request_when_can_cancel_request_cancels_request(
    client_query, auth_headers, requested_friend, user
):
    """Should cancel a friend request to the user when a request has been sent by the user."""

    variables = {"toFriend": requested_friend.uuid}
    client_query(
        CANCEL_FRIEND_REQUEST_MUTATION,
        op_name="cancelFriendRequest",
        variables=variables,
        headers=auth_headers,
    )

    assert not user.outgoing_friend_requests.is_connected(requested_friend)
    assert not requested_friend.incoming_friend_requests.is_connected(user)


def test_cancel_friend_request_when_can_cancel_request_returns_the_user(
    client_query, auth_headers, requested_friend
):
    """Should return the recipient of the request."""
    variables = {"toFriend": requested_friend.uuid}

    response = client_query(
        CANCEL_FRIEND_REQUEST_MUTATION,
        op_name="cancelFriendRequest",
        variables=variables,
        headers=auth_headers,
    )

    content = response.json()
    data = content.get("data").get("cancelFriendRequest")

    assert data.get("cancelledFriendRequestee").get("uuid") == requested_friend.uuid
    assert data.get("success")
    assert not data.get("errors")


def test_cancel_friend_requests_when_already_friends_does_nothing(
    snapshot, client_query, auth_headers, requested_friend, user
):
    """Should do nothing when the users are already friends."""
    user.add_friend(requested_friend)
    variables = {"toFriend": requested_friend.uuid}

    response = client_query(
        CANCEL_FRIEND_REQUEST_MUTATION,
        op_name="cancelFriendRequest",
        variables=variables,
        headers=auth_headers,
    )
    content = response.json()

    snapshot.assert_match(content)


def test_cancel_friend_requests_when_addressee_attempts_to_cancel(
    snapshot, client_query, auth_headers, requested_friend, user
):
    """Should do nothing when the addressee attempts to cancel the request."""
    requested_friend.send_friend_request(user)
    variables = {"toFriend": str(user.uuid)}

    response = client_query(
        CANCEL_FRIEND_REQUEST_MUTATION,
        op_name="cancelFriendRequest",
        variables=variables,
        headers=auth_headers,
    )
    content = response.json()

    snapshot.assert_match(content)


def test_cancel_friend_requests_when_unauthenticated_fails(
    snapshot, client_query, requested_friend
):
    """A user should not be able to cancel a friend request when unauthenticated."""
    variables = {"toFriend": requested_friend.uuid}
    response = client_query(
        CANCEL_FRIEND_REQUEST_MUTATION,
        op_name="cancelFriendRequest",
        variables=variables,
    )
    content = response.json()

    snapshot.assert_match(content)


def test_accept_friend_request_when_can_accept_request_accepts_request(
    client_query, auth_headers, requesting_friend, user
):
    """Should accept the friend request from the user when it has been sent to the user."""
    variables = {"requester": requesting_friend.uuid}
    client_query(
        ACCEPT_FRIEND_REQUEST_MUTATION,
        op_name="acceptFriendRequest",
        variables=variables,
        headers=auth_headers,
    )

    assert user.friends.is_connected(requesting_friend)
    assert user.following.is_connected(requesting_friend)
    assert requesting_friend.friends.is_connected(user)
    assert requesting_friend.following.is_connected(user)


def test_accept_friend_request_when_can_accept_request_returns_the_user(
    client_query, auth_headers, requesting_friend
):
    """Should return the recipient of the request when successful."""
    variables = {"requester": requesting_friend.uuid}
    response = client_query(
        ACCEPT_FRIEND_REQUEST_MUTATION,
        op_name="acceptFriendRequest",
        variables=variables,
        headers=auth_headers,
    )

    content = response.json()
    data = content.get("data").get("acceptFriendRequest")

    assert data.get("friend").get("uuid") == requesting_friend.uuid
    assert data.get("success")
    assert not data.get("errors")


def test_accept_friend_requests_when_already_friends_does_nothing(
    snapshot, client_query, auth_headers, requesting_friend, user
):
    """Should return the friend when the users are already friends."""
    user.add_friend(requesting_friend)
    variables = {"requester": requesting_friend.uuid}

    response = client_query(
        ACCEPT_FRIEND_REQUEST_MUTATION,
        op_name="acceptFriendRequest",
        variables=variables,
        headers=auth_headers,
    )
    content = response.json()
    data = content.get("data").get("acceptFriendRequest")

    assert data.get("friend").get("uuid") == requesting_friend.uuid
    assert data.get("success")
    assert not data.get("errors")


def test_accept_friend_requests_when_addressee_attempts_to_accept(
    snapshot, client_query, requesting_friend, user
):
    """Should do nothing when the addressee attempts to accept on behalf of the user."""
    variables = {"requester": requesting_friend.uuid}
    account = Account.objects.get(id=requesting_friend.uuid)
    # token = f"{jwt_settings.JWT_AUTH_HEADER_PREFIX} {get_token(account)}"
    # auth_headers = {jwt_settings.JWT_AUTH_HEADER_NAME: token}

    response = client_query(
        ACCEPT_FRIEND_REQUEST_MUTATION,
        op_name="acceptFriendRequest",
        variables=variables,
        # headers=auth_headers,
    )
    content = response.json()

    snapshot.assert_match(content)


def test_accept_friend_requests_when_unauthenticated_fails(
    snapshot, client_query, requesting_friend
):
    """A user should not be able to accept a friend request when unauthenticated."""
    variables = {"requester": requesting_friend.uuid}
    response = client_query(
        ACCEPT_FRIEND_REQUEST_MUTATION,
        op_name="acceptFriendRequest",
        variables=variables,
    )
    content = response.json()

    snapshot.assert_match(content)


def test_unfriend_user_when_friends_unfriends_user(
    client_query, user, friend, auth_headers
):
    """Should remove the users as friends and unfollow each other."""
    variables = {"friend": friend.uuid}
    client_query(
        UNFRIEND_USER_MUTATION,
        op_name="unfriendUser",
        variables=variables,
        headers=auth_headers,
    )

    assert not user.friends.is_connected(friend)
    assert not user.following.is_connected(friend)
    assert not user.followed_by.is_connected(friend)


def test_unfriend_user_when_friends_returns_unfriended_user(
    client_query, user, friend, auth_headers
):
    """Should return the user who was unfriended."""
    variables = {"friend": friend.uuid}
    response = client_query(
        UNFRIEND_USER_MUTATION,
        op_name="unfriendUser",
        variables=variables,
        headers=auth_headers,
    )
    content = response.json()
    print(content)
    data = content.get("data").get("unfriendUser")

    assert data.get("unfriendedPerson").get("uuid") == friend.uuid
    assert data.get("success")
    assert not data.get("errors")


def test_unfriend_user_when_not_friends_returns_error(
    snapshot, client_query, user, auth_headers
):
    """Should return an error if the users are not friends."""
    non_friend = UserFactory()
    variables = {"friend": non_friend.uuid}
    response = client_query(
        UNFRIEND_USER_MUTATION,
        op_name="unfriendUser",
        variables=variables,
        headers=auth_headers,
    )
    content = response.json()

    snapshot.assert_match(content)


def test_unfriend_user_when_user_attempts_to_unfriend_itself(
    snapshot, client_query, user, auth_headers
):
    """Should return an error if the user attempts to unfriend itself."""
    variables = {"friend": str(user.uuid)}
    response = client_query(
        UNFRIEND_USER_MUTATION,
        op_name="unfriendUser",
        variables=variables,
        headers=auth_headers,
    )
    content = response.json()

    snapshot.assert_match(content)


def test_unfriend_user_when_unauthenticated(snapshot, client_query, friend):
    """Should not be able to unfriend another user when unauthenticated."""
    variables = {"friend": friend.uuid}
    response = client_query(
        UNFRIEND_USER_MUTATION, op_name="unfriendUser", variables=variables
    )
    content = response.json()

    snapshot.assert_match(content)


def test_unfollow_friend_when_friends_unfollows_friend(
    client_query, user, friend, auth_headers
):
    """Should unfollow the friend when the users are friends."""
    variables = {"friendId": friend.uuid}
    client_query(
        UNFOLLOW_FRIEND_MUTATION,
        op_name="unfollowFriend",
        variables=variables,
        headers=auth_headers,
    )

    assert not user.following.is_connected(friend)
    assert user.friends.is_connected(friend)


def test_unfollow_friend_when_friends_returns_unfollowed_friend(
    client_query, user, friend, auth_headers
):
    """Should return the unfollowed friend when the users are friends."""
    variables = {"friendId": friend.uuid}
    response = client_query(
        UNFOLLOW_FRIEND_MUTATION,
        op_name="unfollowFriend",
        variables=variables,
        headers=auth_headers,
    )
    content = response.json(object_hook=lambda d: SimpleNamespace(**d))
    data = content.data.unfollowFriend

    assert data.unfollowedFriend.uuid == friend.uuid
    assert data.success
    assert not data.errors


def test_unfollow_friend_when_not_friends(snapshot, client_query, auth_headers):
    """Should return an error when the users are not friends."""
    non_friend = UserFactory()
    variables = {"friendId": non_friend.uuid}
    response = client_query(
        UNFOLLOW_FRIEND_MUTATION,
        op_name="unfollowFriend",
        variables=variables,
        headers=auth_headers,
    )
    content = response.json()

    snapshot.assert_match(content)


def test_unfollow_friend_when_friend_does_not_exist(
    snapshot, client_query, auth_headers
):
    """Should return an error when the friend does not exist."""
    non_friend = UserFactory.build()
    variables = {"friendId": non_friend.uuid}
    response = client_query(
        UNFOLLOW_FRIEND_MUTATION,
        op_name="unfollowFriend",
        variables=variables,
        headers=auth_headers,
    )
    content = response.json()

    snapshot.assert_match(content)


def test_unfollow_friend_when_unauthenticated(snapshot, client_query, friend):
    """Should return an error when the user is unauthenticated."""
    variables = {"friendId": friend.uuid}
    response = client_query(
        UNFOLLOW_FRIEND_MUTATION, op_name="unfollowFriend", variables=variables
    )
    content = response.json()

    snapshot.assert_match(content)


def test_follow_friend_when_friends_follows_friend(
    client_query, user, friend, auth_headers
):
    """Should follow the friend when the users are friends."""
    user.following.disconnect(friend)

    variables = {"friendId": friend.uuid}
    client_query(
        FOLLOW_FRIEND_MUTATION,
        op_name="followFriend",
        variables=variables,
        headers=auth_headers,
    )

    assert user.following.is_connected(friend)
    assert user.friends.is_connected(friend)


def test_follow_friend_when_friends_returns_followed_friend(
    client_query, user, friend, auth_headers
):
    """Should return the followed friend when the users are friends."""
    user.following.disconnect(friend)

    variables = {"friendId": friend.uuid}
    response = client_query(
        FOLLOW_FRIEND_MUTATION,
        op_name="followFriend",
        variables=variables,
        headers=auth_headers,
    )
    content = response.json(object_hook=lambda d: SimpleNamespace(**d))
    data = content.data.followFriend

    assert data.followedFriend.uuid == friend.uuid
    assert data.success
    assert not data.errors


def test_follow_friend_when_not_friends(snapshot, client_query, auth_headers):
    """Should return an error when the users are not friends."""
    non_friend = UserFactory()
    variables = {"friendId": non_friend.uuid}
    response = client_query(
        FOLLOW_FRIEND_MUTATION,
        op_name="followFriend",
        variables=variables,
        headers=auth_headers,
    )
    content = response.json()

    snapshot.assert_match(content)


def test_follow_friend_when_friend_does_not_exist(snapshot, client_query, auth_headers):
    """Should return an error when the friend does not exist."""
    non_friend = UserFactory.build()
    variables = {"friendId": non_friend.uuid}
    response = client_query(
        FOLLOW_FRIEND_MUTATION,
        op_name="followFriend",
        variables=variables,
        headers=auth_headers,
    )
    content = response.json()

    snapshot.assert_match(content)


def test_follow_friend_when_unauthenticated(snapshot, client_query, friend):
    """Should return an error when the user is unauthenticated."""
    variables = {"friendId": friend.uuid}
    response = client_query(
        FOLLOW_FRIEND_MUTATION, op_name="followFriend", variables=variables
    )
    content = response.json()

    snapshot.assert_match(content)
