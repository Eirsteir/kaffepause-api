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

CANCEL_FRIEND_REQUEST_MUTATION = """
    mutation cancelFriendRequest($toFriend: String!) {
        cancelFriendRequest(toFriend: $toFriend) {
            cancelledFriendRequestee {
                uuid
            }
            success
            errors
        }
    }
"""

ACCEPT_FRIEND_REQUEST_MUTATION = """
    mutation acceptFriendRequest($requester: String!) {
        acceptFriendRequest(requester: $requester) {
            friend {
                uuid
            }
            success
            errors
        }
    }
"""

UNFRIEND_USER_MUTATION = """
    mutation unfriendUser($friend: String!) {
        unfriendUser(friend: $friend) {
            unfriendedPerson {
                uuid
            }
            success
            errors
        }
    }
"""

UNFOLLOW_FRIEND_MUTATION = """
    mutation unfollowFriend($friendId: UUID!) {
        unfollowFriend(friendId: $friendId) {
            unfollowedFriend {
                uuid
            }
            success
            errors
        }
    }
"""

FOLLOW_FRIEND_MUTATION = """
    mutation followFriend($friendId: UUID!) {
        followFriend(friendId: $friendId) {
            followedFriend {
                uuid
            }
            success
            errors
        }
    }
"""
