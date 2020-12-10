import graphene
from graphene_django.debug import DjangoDebug

import kaffepause.accounts.schema
import kaffepause.breaks.schema
import kaffepause.relationships.schema
import kaffepause.statusupdates.schema
import kaffepause.users.schema


class Query(
    kaffepause.accounts.schema.Query,
    kaffepause.users.schema.Query,
    kaffepause.relationships.schema.Query,
    kaffepause.breaks.schema.Query,
    graphene.ObjectType,
):
    debug = graphene.Field(DjangoDebug, name="__debug")


class Mutation(
    kaffepause.accounts.schema.Mutation,
    kaffepause.users.schema.Mutation,
    kaffepause.relationships.schema.Mutation,
    kaffepause.breaks.schema.Mutation,
    kaffepause.statusupdates.schema.Mutation,
    graphene.ObjectType,
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
