import graphene
from django.contrib.auth import get_user_model
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from kaffepause.relationships.models import Relationship

User = get_user_model()


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        filter_fields = {
            "id": ["exact"],
            "name": ["exact", "icontains", "istartswith"],
            "username": ["exact", "icontains", "istartswith"],
            "friends": ["exact"],
            "friends__name": ["exact"],
        }
        interfaces = (relay.Node,)


class RelationshipNode(DjangoObjectType):
    class Meta:
        model = Relationship
        filter_fields = ("from_user", "to_user", "since")
        interfaces = (relay.Node,)


class Query(graphene.ObjectType):
    user = relay.Node.Field(UserNode)
    all_users = DjangoFilterConnectionField(UserNode)

    relationship = relay.Node.Field(RelationshipNode)
    all_relationships = DjangoFilterConnectionField(RelationshipNode)

    def resolve_all_users(root, info):
        return User.objects.all()


schema = graphene.Schema(query=Query)
