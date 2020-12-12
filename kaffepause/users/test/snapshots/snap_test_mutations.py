# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_update_profile_when_unauthenticated 1"] = {
    "data": {"updateProfile": None},
    "errors": [
        {
            "locations": [{"column": 7, "line": 3}],
            "message": "You do not have permission to perform this action",
            "path": ["updateProfile"],
        }
    ],
}
