from typing import List
from uuid import UUID
from django.utils.translation import gettext_lazy as _

from django.core.exceptions import PermissionDenied
from django.utils import timezone
from neomodel import db

from kaffepause.breaks.enums import BreakRelationship
from kaffepause.breaks.models import Break, BreakInvitation
from kaffepause.users.models import User


def can_user_edit_break(user: User, break_: Break) -> bool:
    return is_viewer_initiator(actor=user, break_=break_) and not break_.has_passed


def is_viewer_initiator(*, actor, break_: Break):
    return actor.is_initiator_of(break_)


def get_break_title(*, actor: User, break_: Break) -> str:
    if break_.has_passed:
        return _("Du tok en pause")

    if actor.is_initiator_of(break_=break_) and break_.get_invitation().has_addressees:
        return _("Du har invitert til pause")

    if actor.is_initiator_of(break_=break_) or actor.is_participant_of(break_=break_):
        return _("Du skal ta en pause")

    if actor.is_invited_to(break_=break_):
        return _("%(sender_name)s inviterte deg til pause" % {"sender_name": break_.get_invitation().get_sender().short_name})

    return _("Pause")


def get_next_break(actor: User) -> Break:
    """Return the next break in time where actor is a participant."""
    return actor.breaks.filter(starting_at__gt=timezone.now()).first_or_none()


def get_break(actor: User, uuid: UUID) -> Break:
    query = f"""
    MATCH
        (b:Break {{uuid: $break_uuid}}),
        (u:User {{uuid: $user_uuid}})
    WHERE (u)-[:{BreakRelationship.PARTICIPATED_IN}]->(b)
        OR (u)-[:{BreakRelationship.SENT} | :{BreakRelationship.TO}]-(:BreakInvitation)-[:{BreakRelationship.REGARDING}]->(b)
    RETURN b
    """
    params = dict(break_uuid=str(uuid), user_uuid=str(actor.uuid))
    results, meta = db.cypher_query(query, params, resolve_objects=True)

    if not results:
        raise PermissionDenied

    return results[0][0]


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
    query += "RETURN break_"
    params = dict(user_uuid=str(actor.uuid))
    results, meta = db.cypher_query(query, params=params)
    breaks = [Break.inflate(row[0]) for row in results]
    return breaks


def get_upcoming_breaks(actor: User) -> List[Break]:
    return actor.breaks.filter(starting_at__gt=timezone.now())


def get_break_history(actor: User) -> List[Break]:
    return actor.breaks.filter(starting_at__lt=timezone.now())
