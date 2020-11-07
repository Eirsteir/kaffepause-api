import graphene
from graphene_django.debug import DjangoDebug

import kaffepause.users.schema


class Query(
    kaffepause.users.schema.Query,
    graphene.ObjectType,
):
    debug = graphene.Field(DjangoDebug, name="__debug")


schema = graphene.Schema(query=Query)
