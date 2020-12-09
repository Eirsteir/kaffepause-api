import graphene
from graphene import relay


class StatusUpdateNode(graphene.ObjectType):
    class Meta:
        interfaces = (relay.Node,)
        name = "StatusUpdate"

    type = graphene.String()
    created = graphene.DateTime()
