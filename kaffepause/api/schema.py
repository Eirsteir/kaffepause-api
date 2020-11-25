import graphene
from graphene_django.debug import DjangoDebug

import kaffepause.breaks.schema
import kaffepause.friendships.schema
import kaffepause.users.schema


class Query(
    kaffepause.users.schema.Query,
    kaffepause.friendships.schema.Query,
    kaffepause.breaks.schema.Query,
    graphene.ObjectType,
):
    debug = graphene.Field(DjangoDebug, name="__debug")


class Mutation(
    kaffepause.users.schema.Mutation,
    kaffepause.friendships.schema.Mutation,
    kaffepause.breaks.schema.Mutation,
    graphene.ObjectType,
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
