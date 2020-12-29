# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_update_profile_when_unauthenticated 1"] = {
    "data": {"updateProfile": None},
    "errors": [
        {
            "locations": [{"column": 7, "line": 8}],
            "message": "You do not have permission to perform this action",
            "path": ["updateProfile"],
        }
    ],
}

snapshots["test_update_profile_when_username_already_in_use 1"] = {
    "data": {"updateProfile": None},
    "errors": [
        {
            "locations": [{"column": 7, "line": 8}],
            "message": "{'username': ['This username has already been taken.']}",
            "path": ["updateProfile"],
        }
    ],
}
