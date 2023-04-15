from uuid import UUID

import graphene

from kaffepause.breaks.models import BreakInvitation
from kaffepause.breaks.services import (
    accept_break_invitation,
    create_break_and_invitation,
    decline_break_invitation, ignore_break_invitation,
)
from kaffepause.breaks.types import BreakInvitationNode, BreakNode
from kaffepause.common.bases import LoginRequiredMixin, NeomodelGraphQLMixin, Output


class InitiateBreak(
    LoginRequiredMixin, NeomodelGraphQLMixin, Output, graphene.Mutation
):
    class Arguments:
        addressees = graphene.List(graphene.UUID, required=False)
        start_time = graphene.DateTime(required=False)
        location = graphene.UUID(required=False)

    break_ = graphene.Field(BreakNode)

    @classmethod
    def resolve_mutation(cls, root, info, addressees=None, start_time=None, location=None):
        current_user = cls.get_current_user()
        break_ = create_break_and_invitation(
            actor=current_user, addressees=addressees, starting_at=start_time, location=location
        )
        return cls(break_=break_, success=True)


class BreakInvitationAction(
    LoginRequiredMixin, NeomodelGraphQLMixin, Output, graphene.Mutation
):
    class Arguments:
        invitation = graphene.UUID()

    _invitation_action = None

    # TODO: Return invitation or break?
    invitation = graphene.Field(BreakInvitationNode)

    @classmethod
    def resolve_mutation(cls, root, info, invitation):
        invitation = BreakInvitation.nodes.get(uuid=invitation)
        current_user = cls.get_current_user()
        invitation = cls._invitation_action(actor=current_user, invitation=invitation)
        return cls(invitation=invitation, success=True)


class AcceptBreakInvitation(BreakInvitationAction):
    _invitation_action = accept_break_invitation


class DeclineBreakInvitation(BreakInvitationAction):
    _invitation_action = decline_break_invitation


class IgnoreBreakInvitation(BreakInvitationAction):
    _invitation_action = ignore_break_invitation
