import uuid

import graphene
from django.contrib.auth import get_user_model
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from kaffepause.relationships.models import Relationship, RelationshipStatus
from kaffepause.relationships.selectors import get_friends
from kaffepause.relationships.services import create_relationship

User = get_user_model()


class UUIDNode(
    relay.Node
):  # extends graphene.relay.Node and returns a non-encoded ID
    class Meta:
        name = "UUIDNode"

    @staticmethod
    def to_global_id(type, id):
        return id


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        fields = (
            "id",
            "name",
            "username",
            "friends",
            "to_users",
            "from_users",
        )
        filter_fields = {
            "id": ["exact"],
            "name": ["exact", "icontains", "istartswith"],
            "username": ["exact", "icontains", "istartswith"],
            "friends": ["exact"],
            "friends__name": ["exact"],
        }
        interfaces = (UUIDNode,)

    def resolve_friends(parent, info):

        return get_friends(parent)


class RelationshipNode(DjangoObjectType):
    class Meta:
        model = Relationship
        filter_fields = ("from_user", "to_user", "status", "since")
        interfaces = (relay.Node,)


class RelationshipStatusNode(DjangoObjectType):
    class Meta:
        model = RelationshipStatus
        filter_fields = ("name", "verb", "slug")
        interfaces = (relay.Node,)


class Query(graphene.ObjectType):
    user = relay.Node.Field(UserNode)
    all_users = DjangoFilterConnectionField(UserNode)

    relationship = relay.Node.Field(RelationshipNode)
    all_relationships = DjangoFilterConnectionField(RelationshipNode)

    def resolve_all_users(root, info):
        return User.objects.all().prefetch_related("friends")


class SendFriendRequest(graphene.Mutation):
    class Arguments:
        to_friend = graphene.String()

    # This defines the response of the mutation
    relationship = graphene.Field(RelationshipNode)
    ok = graphene.Boolean()

    def mutate(self, info, to_friend):
        current_user = info.context.user
        to_friend = User.objects.get(id=to_friend)
        relationship = create_relationship(
            from_user=current_user, to_user=to_friend
        )
        return SendFriendRequest(relationship=relationship, ok=True)


class Mutation:

    send_friend_request = SendFriendRequest.Field()
