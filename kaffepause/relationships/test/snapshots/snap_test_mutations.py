# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_accept_friend_requests_when_addressee_attempts_to_accept 1"] = {
    "data": {"acceptFriendRequest": None},
    "errors": [
        {
            "locations": [{"column": 9, "line": 3}],
            "message": "None",
            "path": ["acceptFriendRequest"],
        }
    ],
}

snapshots["test_accept_friend_requests_when_unauthenticated_fails 1"] = {
    "data": {"acceptFriendRequest": None},
    "errors": [
        {
            "locations": [{"column": 9, "line": 3}],
            "message": "You do not have permission to perform this action",
            "path": ["acceptFriendRequest"],
        }
    ],
}

snapshots["test_cancel_friend_requests_when_addressee_attempts_to_cancel 1"] = {
    "data": {"cancelFriendRequest": None},
    "errors": [
        {
            "locations": [{"column": 9, "line": 3}],
            "message": "None",
            "path": ["cancelFriendRequest"],
        }
    ],
}

snapshots["test_cancel_friend_requests_when_already_friends_does_nothing 1"] = {
    "data": {"cancelFriendRequest": None},
    "errors": [
        {
            "locations": [{"column": 9, "line": 3}],
            "message": "None",
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
            "message": "None",
            "path": ["sendFriendRequest"],
        }
    ],
}

snapshots["test_send_friend_request_when_an_incoming_request_is_already_sent 1"] = {
    "data": {"sendFriendRequest": None},
    "errors": [
        {
            "locations": [{"column": 9, "line": 3}],
            "message": "None",
            "path": ["sendFriendRequest"],
        }
    ],
}

snapshots["test_send_friend_request_when_an_outgoing_request_is_already_sent 1"] = {
    "data": {"sendFriendRequest": None},
    "errors": [
        {
            "locations": [{"column": 9, "line": 3}],
            "message": "None",
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

snapshots["test_unfriend_user_when_not_friends_returns_error 1"] = {
    "data": {"unfriendUser": None},
    "errors": [
        {
            "locations": [{"column": 9, "line": 3}],
            "message": "None",
            "path": ["unfriendUser"],
        }
    ],
}

snapshots["test_unfriend_user_when_unauthenticated 1"] = {
    "data": {"unfriendUser": None},
    "errors": [
        {
            "locations": [{"column": 9, "line": 3}],
            "message": "You do not have permission to perform this action",
            "path": ["unfriendUser"],
        }
    ],
}

snapshots["test_unfriend_user_when_user_attempts_to_unfriend_itself 1"] = {
    "data": {"unfriendUser": None},
    "errors": [
        {
            "locations": [{"column": 9, "line": 3}],
            "message": "None",
            "path": ["unfriendUser"],
        }
    ],
}
