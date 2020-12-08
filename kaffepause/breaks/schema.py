import graphene
from graphene import relay

from kaffepause.breaks.mutations import (
    AcceptBreakInvitation,
    DeclineBreakInvitation,
    InitiateBreak,
)
from kaffepause.breaks.selectors import (
    get_all_break_invitations,
    get_break_invitations_awaiting_reply,
    get_expired_break_invitations,
)
from kaffepause.breaks.types import BreakInvitationConnection
from kaffepause.common.bases import NeomodelGraphQLMixin


class Query(NeomodelGraphQLMixin, graphene.ObjectType):

    break_invitations_awaiting_reply = relay.ConnectionField(BreakInvitationConnection)
    expired_break_invitations = relay.ConnectionField(BreakInvitationConnection)
    all_break_invitations = relay.ConnectionField(BreakInvitationConnection)

    def resolve_break_invitations_awaiting_reply(root, info):
        current_user = root.get_current_user(info)
        return get_break_invitations_awaiting_reply(actor=current_user)

    def resolve_expired_break_invitations(root, info):
        current_user = root.get_current_user(info)
        return get_expired_break_invitations(actor=current_user)

    def resolve_all_break_invitations(root, info):
        current_user = root.get_current_user(info)
        return get_all_break_invitations(actor=current_user)


class Mutation(graphene.ObjectType):

    invite_friends_to_a_break = InitiateBreak.Field()
    accept_break_invitation = AcceptBreakInvitation.Field()
    decline_break_invitation = DeclineBreakInvitation.Field()
