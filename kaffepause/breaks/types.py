import graphene
from graphene import relay

from kaffepause.common.types import CountableConnection
from kaffepause.users.types import UserConnection, UserNode


class BreakInvitationNode(graphene.ObjectType):
    class Meta:
        interfaces = (relay.Node,)
        name = "BreakInvitation"

    uid = graphene.String()
    created = graphene.DateTime()
    sender = graphene.Field(UserNode)
    addressee_count = graphene.Int()
    subject = graphene.Field(lambda: BreakNode)


class BreakNode(graphene.ObjectType):
    class Meta:
        interfaces = (relay.Node,)
        name = "Break"

    uid = graphene.String()
    start_time = graphene.DateTime()
    participants = relay.ConnectionField(UserConnection)
    invitation = graphene.Field(BreakInvitationNode)


class BreakInvitationConnection(CountableConnection):
    class Meta:
        node = BreakInvitationNode
