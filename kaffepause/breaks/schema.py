import graphene
from django.contrib.auth import get_user_model
from graphene_django.filter import DjangoFilterConnectionField

from kaffepause.breaks.types import BreakInvitationType

UserModel = get_user_model()


class Query(graphene.ObjectType):
    # requiring_action?
    pending_break_invitations = DjangoFilterConnectionField(BreakInvitationType)
    previous_break_invitations = DjangoFilterConnectionField(BreakInvitationType)
    all_break_invitations = DjangoFilterConnectionField(BreakInvitationType)
    outgoing_break_invitations = DjangoFilterConnectionField(BreakInvitationType)

    def resolve_pending_break_invitations(parent, info):
        pass

    def resolve_previous_break_invitations(parent, info):
        pass

    def resolve_all_break_invitations(parent, info):
        pass

    def resolve_outgoing_break_invitations(parent, info):
        pass


class Mutation(graphene.ObjectType):
    pass
