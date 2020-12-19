import graphene
from graphene import relay
from neomodel import Q

from kaffepause.common.bases import NeomodelGraphQLMixin
from kaffepause.common.decorators import login_required
from kaffepause.users.models import User
from kaffepause.users.mutations import UpdateProfile
from kaffepause.users.types import UserConnection, UserNode


class UserQuery(NeomodelGraphQLMixin, graphene.ObjectType):

    user = graphene.Field(UserNode, id=graphene.UUID())
    search_users = relay.ConnectionField(UserConnection, q=graphene.String())

    def resolve_user(root, info, id):
        return User.nodes.get(uuid=id)

    @classmethod
    @login_required
    def resolve_search_users(cls, root, info, **kwargs):
        q = kwargs.get("query")
        query = Q(name__icontains=q) | Q(username__icontains=q)
        current_user_uuid = cls.get_current_user().uuid

        users = User.nodes.filter(query).exclude(uuid=current_user_uuid)
        return users


class MeQuery(graphene.ObjectType):
    me = graphene.Field(UserNode)

    def resolve_me(root, info):
        user = info.context.user
        if user.is_authenticated:
            return User.nodes.get(uuid=user.id)
        return None


class ProfileMutation(graphene.ObjectType):
    update_profile = UpdateProfile.Field()


class Query(UserQuery, MeQuery, graphene.ObjectType):
    pass


class Mutation(ProfileMutation, graphene.ObjectType):
    pass
