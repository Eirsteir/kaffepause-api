import graphene
from django.contrib.auth import get_user_model
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from kaffepause.common.schema import UUIDNode
from kaffepause.friendships.selectors import get_friends

User = get_user_model()


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        fields = (
            "id",
            "name",
            "username",
            "friends",
        )
        filter_fields = {
            "id": ["exact"],
            "name": ["exact", "icontains", "istartswith"],
            "username": ["exact", "icontains", "istartswith"],
            "friends": ["exact"],
            "friends__name": ["exact"],
        }
        interfaces = (UUIDNode,)

    # profile_action = graphene.Field(ProfileAction)

    # TODO: enable when adding login required
    # friendship_status = graphene.String()
    #
    # def resolve_friendship_status(parent, info):
    #     current_user = info.context.to_user
    #     return get_friendship_status(to_user=current_user, to_user=parent)

    def resolve_friends(parent, info):

        return get_friends(parent)


class Query(graphene.ObjectType):

    user = relay.Node.Field(UserNode)
    all_users = DjangoFilterConnectionField(UserNode)

    def resolve_all_users(root, info):
        # current_user = info.context.user
        return User.objects.all()  # .exclude(current_user)
