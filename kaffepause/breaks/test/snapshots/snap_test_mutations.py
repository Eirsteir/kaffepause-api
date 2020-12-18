# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_accept_break_invitation_when_unauthenticated_fails 1"] = {
    "data": {"acceptBreakInvitation": None},
    "errors": [
        {
            "locations": [{"column": 9, "line": 3}],
            "message": "You do not have permission to perform this action",
            "path": ["acceptBreakInvitation"],
        }
    ],
}

snapshots["test_decline_break_invitation_when_unauthenticated_fails 1"] = {
    "data": {"declineBreakInvitation": None},
    "errors": [
        {
            "locations": [{"column": 9, "line": 3}],
            "message": "You do not have permission to perform this action",
            "path": ["declineBreakInvitation"],
        }
    ],
}

snapshots["test_initiate_break_when_unauthenticated_fails 1"] = {
    "data": {"initiateBreak": None},
    "errors": [
        {
            "locations": [{"column": 9, "line": 3}],
            "message": "You do not have permission to perform this action",
            "path": ["initiateBreak"],
        }
    ],
}
