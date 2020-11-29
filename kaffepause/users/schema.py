import graphene
from graphene import relay

from kaffepause.common.types import CountingNodeConnection
from kaffepause.users import mutations
from kaffepause.users.models import User
from kaffepause.users.types import UserType


class UserConnection(CountingNodeConnection, relay.Connection):
    class Meta:
        node = UserType


class UserQuery(graphene.ObjectType):

    user = graphene.Field(UserType, id=graphene.String())
    users = relay.ConnectionField(UserConnection)

    def resolve_user(root, info, id):
        return User.nodes.get(uid=id)

    def resolve_users(root, info, **kwargs):
        return User.nodes.all()


class MeQuery(graphene.ObjectType):
    me = graphene.Field(UserType)

    def resolve_me(self, info):
        user = info.context.user
        if user.is_authenticated:
            return User.nodes.get(uid=user.id)
        return None


class ProfileMutations(graphene.ObjectType):
    update_account = mutations.UpdateProfile.Field()


class Query(UserQuery, MeQuery, graphene.ObjectType):
    pass


class Mutation(graphene.ObjectType):
    pass
