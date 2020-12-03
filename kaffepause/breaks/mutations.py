import graphene
from django.contrib.auth import get_user_model

from kaffepause.breaks.models import BreakInvitation
from kaffepause.breaks.services import (
    accept_break_invitation,
    create_and_invite_friends_to_a_break,
    decline_break_invitation,
    ignore_break_invitation,
)
from kaffepause.breaks.types import BreakInvitationNode, BreakNode
from kaffepause.common.bases import Mutation

UserModel = get_user_model()


class InviteFriendsToABreak(Mutation):
    class Arguments:
        start_time = graphene.DateTime(required=False)

    subject = graphene.Field(BreakNode)

    @classmethod
    def resolve_mutation(cls, root, info, start_time=None):
        current_user = info.context.user
        subject = create_and_invite_friends_to_a_break(
            actor=current_user, start_time=start_time
        )
        return cls(subject=subject, success=True)


class BreakInvitationAction(Mutation):
    class Arguments:
        invitation = graphene.String()

    _invitation_action = None

    subject = graphene.Field(BreakNode)
    invitation = graphene.Field(BreakInvitationNode)

    @classmethod
    def resolve_mutation(cls, root, info, invitation):  # TODO: Handle errors
        current_user = info.context.user
        invitation = BreakInvitation.objects.get(id=invitation)
        invitation = cls._invitation_action(actor=current_user, invitation=invitation)
        return cls(subject=invitation.subject, invitation=invitation, success=True)


class AcceptBreakInvitation(BreakInvitationAction):
    _invitation_action = accept_break_invitation


class DeclineBreakInvitation(BreakInvitationAction):
    _invitation_action = decline_break_invitation


class IgnoreBreakInvitation(BreakInvitationAction):
    _invitation_action = ignore_break_invitation
