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

INITIATE_BREAK_MUTATION = """
    mutation initiateBreak($addressees: [UUID], $startTime: DateTime) {
        initiateBreak(addressees: $addressees, startTime: $startTime) {
            break_ {
                uuid
                startingAt
                invitation {
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
                participants {
                    count
                    edges {
                        node {
                            uuid
                        }
                    }
                }
            }
            success
            errors
        }
    }
"""

ACCEPT_BREAK_INVITATION_MUTATION = """
    mutation acceptBreakInvitation($invitation: UUID) {
        acceptBreakInvitation(invitation: $invitation) {
            invitation {
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
            success
            errors
        }
    }
"""

DECLINE_BREAK_INVITATION_MUTATION = """
    mutation declineBreakInvitation($invitation: UUID) {
        declineBreakInvitation(invitation: $invitation) {
            invitation {
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
            success
            errors
        }
    }
"""
