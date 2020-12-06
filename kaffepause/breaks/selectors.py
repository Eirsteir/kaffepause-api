from datetime import datetime, timedelta
from itertools import chain
from typing import List

import pytz
from django.db.models import Q
from django.utils import timezone
from neomodel import db

from kaffepause.breaks.enums import BreakRelationship
from kaffepause.breaks.models import Break, BreakInvitation
from kaffepause.common.typing import QuerySet
from kaffepause.users.models import User


def get_break_invitations_awaiting_reply(actor: User) -> List[BreakInvitation]:
    """Returns all non-expired break invitations awaiting reply."""
    query = f"""
    MATCH (invitation:BreakInvitation)-[:{BreakRelationship.TO}]->(user:User {{uid: {{user_uid}}}})
    MATCH (invitation)-[:{BreakRelationship.REGARDING}]->(break_:Break)
    WHERE NOT (user)-[:{BreakRelationship.ACCEPTED} | :{BreakRelationship.DECLINED}]->(invitation)
    AND break_.start_time > datetime().epochSeconds - (60*5) // 5 minutes ago
    RETURN invitation
    """
    params = dict(user_uid=actor.uid)
    results, meta = db.cypher_query(query, params=params)
    unanswered_invitations = [BreakInvitation.inflate(row[0]) for row in results]
    return unanswered_invitations


def get_expired_break_invitations(actor: User) -> QuerySet[BreakInvitation]:
    raise NotImplementedError


def get_all_break_invitations(actor: User) -> QuerySet[BreakInvitation]:
    raise NotImplementedError


def _get_incoming_query(user: User) -> Q:
    raise NotImplementedError


def get_outgoing_break_invitations(actor: User) -> QuerySet[BreakInvitation]:
    raise NotImplementedError
