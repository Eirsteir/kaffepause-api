# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_delete_account 1"] = {
    "data": {"deleteAccount": {"errors": None, "success": True}}
}

snapshots["test_delete_account_unauthenticated 1"] = {
    "data": {
        "deleteAccount": {
            "errors": {
                "nonFieldErrors": [
                    {"code": "unauthenticated", "message": "Unauthenticated."}
                ]
            },
            "success": False,
        }
    }
}
