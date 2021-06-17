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


def get_all_break_invitations(actor: User) -> List[BreakInvitation]:
    return actor.break_invitations.all()


def get_pending_break_invitations(actor: User) -> List[BreakInvitation]:
    """Returns all non-expired unanswered break invitations."""
    query = (
        _get_unanswered_invitations_query()
        + f"""
    AND break_.starting_at > {_get_cypher_minutes_ago(5)}
    """
    )
    unanswered_invitations = _run_break_invitation_query(query, actor)
    return unanswered_invitations


def get_expired_break_invitations(actor: User) -> List[BreakInvitation]:
    query = (
        _get_unanswered_invitations_query()
        + f"""
    AND break_.starting_at < {_get_cypher_minutes_ago(5)}
    """
    )
    unanswered_invitations = _run_break_invitation_query(query, actor)
    return unanswered_invitations


def _get_unanswered_invitations_query() -> str:
    query = f"""
    MATCH (invitation:BreakInvitation)-[:{BreakRelationship.TO}]->(user:User {{uuid: $user_uuid}})
    MATCH (invitation)-[:{BreakRelationship.REGARDING}]->(break_:Break)
    WHERE NOT (user)-[:{BreakRelationship.ACCEPTED} | {BreakRelationship.DECLINED}]->(invitation)
    """
    return query


def _get_cypher_minutes_ago(minutes) -> str:
    return f"datetime().epochSeconds - (60*{minutes})"


def _run_break_invitation_query(query: str, actor: User) -> List[BreakInvitation]:
    query += "RETURN invitation"
    params = dict(user_uuid=str(actor.uuid))
    results, meta = db.cypher_query(query, params=params)
    break_invitations = [BreakInvitation.inflate(row[0]) for row in results]
    return break_invitations


def get_break_history(actor: User) -> List[Break]:
    return actor.breaks.filter(starting_at__lt=timezone.now())
