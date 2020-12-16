# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_all_break_invitations_unauthenticated 1"] = {
    "data": {"allBreakInvitations": None},
    "errors": [
        {
            "locations": [{"column": 7, "line": 3}],
            "message": "You do not have permission to perform this action",
            "path": ["allBreakInvitations"],
        }
    ],
}

snapshots["test_expired_break_invitations_unauthenticated 1"] = {
    "data": {"expiredBreakInvitations": None},
    "errors": [
        {
            "locations": [{"column": 7, "line": 3}],
            "message": "You do not have permission to perform this action",
            "path": ["expiredBreakInvitations"],
        }
    ],
}

snapshots["test_pending_break_invitations_unauthenticated_returns_error 1"] = {
    "data": {"pendingBreakInvitations": None},
    "errors": [
        {
            "locations": [{"column": 7, "line": 3}],
            "message": "You do not have permission to perform this action",
            "path": ["pendingBreakInvitations"],
        }
    ],
}
