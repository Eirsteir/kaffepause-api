import graphene
from graphene import relay


class FriendshipNode(graphene.ObjectType):
    class Meta:
        interfaces = (relay.Node,)
        name = "friendship"

    since = graphene.DateTime()

    def resolve_since(self, info):
        return self.since
