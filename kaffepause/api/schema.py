import graphene
from graphene_django.debug import DjangoDebug

import kaffepause.friendships.schema
import kaffepause.users.schema


class Query(
    kaffepause.users.schema.Query,
    kaffepause.friendships.schema.Query,
    graphene.ObjectType,
):
    debug = graphene.Field(DjangoDebug, name="__debug")


class Mutation(
    kaffepause.friendships.schema.Mutation,
    graphene.ObjectType,
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
