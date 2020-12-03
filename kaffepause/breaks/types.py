import graphene
from graphene import relay

from kaffepause.users.types import UserNode


class BreakInvitationNode(graphene.ObjectType):
    class Meta:
        interfaces = (relay.Node,)
        name = "Break Invitation"

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
    participants = relay.ConnectionField(UserNode)
    invitation = graphene.Field(BreakInvitationNode)
