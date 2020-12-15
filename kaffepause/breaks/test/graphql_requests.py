"""Queries and mutations used by the test suite."""

PENDING_BREAK_INVITATIONS_QUERY = """
    query pendingBreakInvitations {
      pendingBreakInvitations {
        edges {
            node {
                uuid
                created
                sender {
                    uuid
                }
                addresseeCount
                subject {
                    uuid
                }
            }
        }
      }
    }
"""
