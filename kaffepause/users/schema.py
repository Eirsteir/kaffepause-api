import graphene
from graphene import relay
from graphene_django import DjangoConnectionField
from graphql_auth import mutations

from kaffepause.users.types import UserType


class UserQuery(graphene.ObjectType):

    user = relay.Node.Field(UserType)
    # users = DjangoConnectionField(User)
    #
    # def resolve_users(parent, info):
    #     return User.nodes.all()


class MeQuery(graphene.ObjectType):
    pass
    # me = graphene.Field(User)
    #
    # def resolve_me(self, info):
    #     user = info.context.user
    #     if user.is_authenticated:
    #         return user
    #     return None


class Query(UserQuery, MeQuery, graphene.ObjectType):
    pass


class Mutation(graphene.ObjectType):
    pass
