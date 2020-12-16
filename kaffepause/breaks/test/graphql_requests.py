"""Queries and mutations used by the test suite."""

PENDING_BREAK_INVITATIONS_QUERY = """
    query pendingBreakInvitations {
      pendingBreakInvitations {
        count
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

ALL_BREAK_INVITATIONS_QUERY = """
    query allBreakInvitations {
      allBreakInvitations {
        count
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

EXPIRED_BREAK_INVITATIONS_QUERY = """
    query expiredBreakInvitations {
      expiredBreakInvitations {
        count
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
