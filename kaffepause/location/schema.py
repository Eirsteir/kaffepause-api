import graphene
from graphene import relay

from kaffepause.common.bases import NeomodelGraphQLMixin
from kaffepause.common.decorators import login_required
from kaffepause.location.mutations import AddUserLocation
from kaffepause.location.selectors import get_campus_locations
from kaffepause.location.types import LocationConnection


class LocationQuery(NeomodelGraphQLMixin, graphene.ObjectType):

    locations = relay.ConnectionField(LocationConnection, query=graphene.String())

    @classmethod
    @login_required
    def resolve_locations(cls, root, info, **kwargs):
        current_user = cls.get_current_user()
        return get_campus_locations(actor=current_user, **kwargs)


class LocationMutations(graphene.ObjectType):
    add_user_location = AddUserLocation.Field()


class Query(LocationQuery, graphene.ObjectType):
    pass


class Mutation(LocationMutations, graphene.ObjectType):
    pass
