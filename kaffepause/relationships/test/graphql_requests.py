"""Queries and mutations used by the test suite."""

SEND_FRIEND_REQUEST_MUTATION = """
    mutation sendFriendRequest($toFriend: String!) {
        sendFriendRequest(toFriend: $toFriend) {
            sentFriendRequestee {
                uuid
            }
            success
            errors
        }
    }
"""
