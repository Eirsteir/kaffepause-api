import graphene
from graphene import relay

from kaffepause.location.mutations import AddUserLocation
from kaffepause.location.selectors import get_campus_locations
from kaffepause.location.types import LocationConnection


class LocationQuery(graphene.ObjectType):

    locations = relay.ConnectionField(LocationConnection, query=graphene.String())

    def resolve_locations(root, info, **kwargs):
        return get_campus_locations(**kwargs)


class LocationMutations(graphene.ObjectType):
    add_user_location = AddUserLocation.Field()


class Query(LocationQuery, graphene.ObjectType):
    pass


class Mutation(LocationMutations, graphene.ObjectType):
    pass
