import graphene
from graphene import relay
from kaffepause.users.types import UserNode


class GroupNode(graphene.ObjectType):
    class Meta:
        interfaces = (relay.Node,)
        name = "Group"

    uuid = graphene.UUID()
    name = graphene.String()
    created = graphene.DateTime()
    creator = graphene.Field(UserNode)
    members = graphene.List(UserNode)

    def resolve_creator(parent, info):
        return parent.creator.single()

    def resolve_members(parent, info):
        return parent.members.all()
