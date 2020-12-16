# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

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
