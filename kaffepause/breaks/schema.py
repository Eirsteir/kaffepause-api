import graphene
from django.contrib.auth import get_user_model

from kaffepause.breaks.mutations import (
    AcceptBreakInvitation,
    DeclineBreakInvitation,
    IgnoreBreakInvitation,
    InviteFriendsToABreak,
)
from kaffepause.breaks.selectors import (
    get_all_break_invitations,
    get_break_invitations_awaiting_reply,
    get_expired_break_invitations,
    get_outgoing_break_invitations,
)
from kaffepause.breaks.types import BreakInvitationType

UserModel = get_user_model()


class Query(graphene.ObjectType):

    # break_invitations_awaiting_reply = DjangoFilterConnectionField(BreakInvitationType)
    # expired_break_invitations = DjangoFilterConnectionField(BreakInvitationType)
    # all_break_invitations = DjangoFilterConnectionField(BreakInvitationType)
    # outgoing_break_invitations = DjangoFilterConnectionField(BreakInvitationType)

    def resolve_break_invitations_awaiting_reply(parent, info):
        current_user = info.context.user
        return get_break_invitations_awaiting_reply(actor=current_user)

    def resolve_expired_break_invitations(parent, info):
        current_user = info.context.user
        return get_expired_break_invitations(actor=current_user)

    def resolve_all_break_invitations(parent, info):
        current_user = info.context.user
        return get_all_break_invitations(actor=current_user)

    def resolve_outgoing_break_invitations(parent, info):
        current_user = info.context.user
        return get_outgoing_break_invitations(actor=current_user)


class Mutation(graphene.ObjectType):

    invite_friends_to_a_break = InviteFriendsToABreak.Field()
    accept_break_invitation = AcceptBreakInvitation.Field()
    decline_break_invitation = DeclineBreakInvitation.Field()
    ignore_break_invitation = IgnoreBreakInvitation.Field()
