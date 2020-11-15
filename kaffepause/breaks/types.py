from graphene import relay
from graphene_django import DjangoObjectType

from kaffepause.breaks.models import BreakInvitation
from kaffepause.common.types import CountingNodeConnection


class BreakInvitationType(DjangoObjectType):
    class Meta:
        model = BreakInvitation
        filter_fields = ("reply", "expiry", "is_seen")
        interfaces = (relay.Node,)
        connection_class = CountingNodeConnection
