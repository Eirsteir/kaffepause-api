import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from kaffepause.friendships.models import Friendship, FriendshipStatus


class FriendshipNode(DjangoObjectType):
    class Meta:
        model = Friendship
        filter_fields = {
            "from_user__username": ["exact"],
            "to_user__username": ["exact"],
            "status__name": ["exact"],
        }
        interfaces = (relay.Node,)

    since = graphene.DateTime()

    def resolve_since(self, info):
        return self.since


class FriendshipStatusNode(DjangoObjectType):
    class Meta:
        model = FriendshipStatus
        filter_fields = ("name", "verb", "from_slug", "to_slug", "slug")
        interfaces = (relay.Node,)
