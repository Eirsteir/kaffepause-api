import graphene
from graphene import relay

from kaffepause.breaks.mutations import (
    AcceptBreakInvitation,
    DeclineBreakInvitation,
    InitiateBreak, IgnoreBreakInvitation,
)
from kaffepause.breaks.selectors import (
    get_all_break_invitations,
    get_break_history,
    get_expired_break_invitations,
    get_pending_break_invitations,
    get_next_break, get_break
)
from kaffepause.breaks.types import (
    BreakConnection,
    BreakInvitationConnection,
    BreakNode, BreaksPresentationNode,
)
from kaffepause.common.bases import NeomodelGraphQLMixin
from kaffepause.common.decorators import login_required


class Query(NeomodelGraphQLMixin, graphene.ObjectType):

    breaks_presentation = graphene.Field(BreaksPresentationNode)
    next_break = graphene.Field(BreakNode)
    break_ = graphene.Field(BreakNode, uuid=graphene.UUID())
    pending_break_invitations = relay.ConnectionField(BreakInvitationConnection)
    expired_break_invitations = relay.ConnectionField(BreakInvitationConnection)
    all_break_invitations = relay.ConnectionField(BreakInvitationConnection)
    break_history = relay.ConnectionField(BreakConnection)

    @classmethod
    @login_required
    def resolve_breaks_presentation(cls, root, info, **kwargs):
        return cls.get_current_user()

    @classmethod
    @login_required
    def resolve_next_break(cls, root, info, **kwargs):
        current_user = cls.get_current_user()
        return get_next_break(actor=current_user)

    @classmethod
    @login_required
    def resolve_break_(cls, root, info, uuid, **kwargs):
        current_user = cls.get_current_user()
        return get_break(actor=current_user, uuid=uuid)

    @classmethod
    @login_required
    def resolve_pending_break_invitations(cls, root, info, **kwargs):
        current_user = cls.get_current_user()
        return get_pending_break_invitations(actor=current_user)

    @classmethod
    @login_required
    def resolve_expired_break_invitations(cls, root, info, **kwargs):
        current_user = cls.get_current_user()
        return get_expired_break_invitations(actor=current_user)

    @classmethod
    @login_required
    def resolve_all_break_invitations(cls, root, info, **kwargs):
        current_user = cls.get_current_user()
        return get_all_break_invitations(actor=current_user)

    @classmethod
    @login_required
    def resolve_break_history(cls, root, info, **kwargs):
        current_user = cls.get_current_user()
        return get_break_history(actor=current_user)


class Mutation(graphene.ObjectType):

    initiate_break = InitiateBreak.Field()
    accept_break_invitation = AcceptBreakInvitation.Field()
    decline_break_invitation = DeclineBreakInvitation.Field()
    ignore_break_invitation = IgnoreBreakInvitation.Field()
