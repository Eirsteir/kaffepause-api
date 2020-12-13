import graphene
from graphene import relay

from kaffepause.users.models import User
from kaffepause.users.mutations import UpdateProfile
from kaffepause.users.types import UserConnection, UserNode


class UserQuery(graphene.ObjectType):

    user = graphene.Field(UserNode, id=graphene.String())
    users = relay.ConnectionField(UserConnection)

    def resolve_user(root, info, id):
        return User.nodes.get(uid=id)

    def resolve_users(root, info, **kwargs):
        return User.nodes.all()


class MeQuery(graphene.ObjectType):
    me = graphene.Field(UserNode)

    def resolve_me(root, info):
        user = info.context.user
        if user.is_authenticated:
            return User.nodes.get(uid=user.id)
        return None


class ProfileMutation(graphene.ObjectType):
    update_profile = UpdateProfile.Field()


class Query(UserQuery, MeQuery, graphene.ObjectType):
    pass


class Mutation(ProfileMutation, graphene.ObjectType):
    pass
