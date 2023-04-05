from datetime import datetime, timedelta
from itertools import chain
from typing import List
from uuid import UUID

import pytz
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from neomodel import db

from kaffepause.breaks.enums import BreakRelationship
from kaffepause.breaks.models import Break, BreakInvitation
from kaffepause.users.models import User


def get_next_break(actor: User) -> Break:
    """Return the next break in time where actor is a participant."""
    print("\n\n\n\nTIMEZONE.NOW(): ----- ", timezone.now(), '\n\n\n\n')
    print("\n\n\n\nTIMEZONE.NOW(): ----- ", timezone.localtime(timezone.now()), '\n\n\n\n')
    return actor.breaks.filter(starting_at__gt=timezone.now()).first_or_none()


def get_break(actor: User, uuid: UUID) -> Break:
    is_invited = actor.break_invitations.filter(uuid=uuid).first_or_none()
    has_participated = actor.breaks.filter(uuid=uuid).first_or_none()

    if not (is_invited or has_participated):
        raise PermissionDenied

    return Break.nodes.get(uuid=uuid)


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
