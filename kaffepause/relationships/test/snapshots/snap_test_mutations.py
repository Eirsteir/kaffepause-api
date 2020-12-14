# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_cancel_friend_requests_when_addressee_attempts_to_cancel 1"] = {
    "data": {"cancelFriendRequest": None},
    "errors": [
        {
            "locations": [{"column": 9, "line": 3}],
            "message": "Cannot cancel this friend request",
            "path": ["cancelFriendRequest"],
        }
    ],
}

snapshots["test_cancel_friend_requests_when_already_friends_does_nothing 1"] = {
    "data": {"cancelFriendRequest": None},
    "errors": [
        {
            "locations": [{"column": 9, "line": 3}],
            "message": "Cannot cancel this friend request. Users are already friends",
            "path": ["cancelFriendRequest"],
        }
    ],
}

snapshots["test_cancel_friend_requests_when_unauthenticated_fails 1"] = {
    "data": {"cancelFriendRequest": None},
    "errors": [
        {
            "locations": [{"column": 9, "line": 3}],
            "message": "You do not have permission to perform this action",
            "path": ["cancelFriendRequest"],
        }
    ],
}

snapshots["test_send_friend_request_when_already_friends_does_not_send_request 1"] = {
    "data": {"sendFriendRequest": None},
    "errors": [
        {
            "locations": [{"column": 9, "line": 3}],
            "message": "Relationship already exists",
            "path": ["sendFriendRequest"],
        }
    ],
}

snapshots["test_send_friend_request_when_an_incoming_request_is_already_sent 1"] = {
    "data": {"sendFriendRequest": None},
    "errors": [
        {
            "locations": [{"column": 9, "line": 3}],
            "message": "Relationship already exists",
            "path": ["sendFriendRequest"],
        }
    ],
}

snapshots["test_send_friend_request_when_an_outgoing_request_is_already_sent 1"] = {
    "data": {"sendFriendRequest": None},
    "errors": [
        {
            "locations": [{"column": 9, "line": 3}],
            "message": "Relationship already exists",
            "path": ["sendFriendRequest"],
        }
    ],
}

snapshots["test_send_friend_request_when_unauthenticated_fails 1"] = {
    "data": {"sendFriendRequest": None},
    "errors": [
        {
            "locations": [{"column": 9, "line": 3}],
            "message": "You do not have permission to perform this action",
            "path": ["sendFriendRequest"],
        }
    ],
}
