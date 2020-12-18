import graphene
from graphene import relay

from kaffepause.common.types import CountableConnection
from kaffepause.users.types import UserConnection, UserNode


class BreakInvitationNode(graphene.ObjectType):
    class Meta:
        interfaces = (relay.Node,)
        name = "BreakInvitation"

    uuid = graphene.String()
    created = graphene.DateTime()
    sender = graphene.Field(UserNode)
    addressee_count = graphene.Int()
    subject = graphene.Field(lambda: BreakNode)

    def resolve_sender(parent, info):
        return parent.get_sender()

    def resolve_addressee_count(parent, info):
        return parent.get_addressee_count()

    def resolve_subject(parent, info):
        return parent.get_subject()


class BreakNode(graphene.ObjectType):
    class Meta:
        interfaces = (relay.Node,)
        name = "Break"

    uuid = graphene.String()
    starting_at = graphene.DateTime()
    participants = relay.ConnectionField(UserConnection)
    invitation = graphene.Field(BreakInvitationNode)

    def resolve_invitation(parent, info):
        return parent.get_invitation()

    def resolve_participants(parent, info):
        return parent.get_participants()


class BreakInvitationConnection(CountableConnection):
    class Meta:
        node = BreakInvitationNode
