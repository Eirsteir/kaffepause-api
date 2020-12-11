"""Queries and mutations used by the test suite."""

UPDATE_STATUS_MUTATION = """
    mutation updateStatus($statusType: StatusUpdateType!) {
        updateStatus(statusType: $statusType) {
            currentStatus {
                statusType
                verb
                created
            }
        }
    }
"""
