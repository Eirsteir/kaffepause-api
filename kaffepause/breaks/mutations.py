import graphene

from kaffepause.breaks.models import BreakInvitation
from kaffepause.breaks.services import (
    accept_break_invitation,
    create_break_and_invitation,
    decline_break_invitation,
)
from kaffepause.breaks.types import BreakInvitationNode, BreakNode
from kaffepause.common.bases import Mutation, NeomodelGraphQLMixin


class InitiateBreak(NeomodelGraphQLMixin, Mutation):
    class Arguments:
        addressees = graphene.List(graphene.String, required=False)
        start_time = graphene.DateTime(required=False)

    break_ = graphene.Field(BreakNode)

    @classmethod
    def resolve_mutation(cls, root, info, addressees=None, start_time=None):
        current_user = cls.get_current_user(info)
        break_ = create_break_and_invitation(
            actor=current_user, addressees=addressees, start_time=start_time
        )
        return cls(break_=break_, success=True)


class BreakInvitationAction(NeomodelGraphQLMixin, Mutation):
    class Arguments:
        invitation = graphene.String()

    _invitation_action = None

    break_ = graphene.Field(BreakNode)
    invitation = graphene.Field(BreakInvitationNode)

    @classmethod
    def resolve_mutation(cls, root, info, invitation):  # TODO: Handle errors
        current_user = cls.get_current_user(info)
        invitation = BreakInvitation.nodes.get(uid=invitation)
        invitation = cls._invitation_action(actor=current_user, invitation=invitation)
        return cls(break_=invitation.get_subject(), invitation=invitation, success=True)


class AcceptBreakInvitation(BreakInvitationAction):
    _invitation_action = accept_break_invitation


class DeclineBreakInvitation(BreakInvitationAction):
    _invitation_action = decline_break_invitation
