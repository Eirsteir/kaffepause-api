import graphene

from kaffepause.common.bases import Mutation
from kaffepause.users.models import User
from kaffepause.users.types import UserType


class UpdateProfile(Mutation):
    class Arguments:
        name = graphene.String(required=True)
        username = graphene.String(required=True)

    user = graphene.Field(UserType)

    @classmethod
    def resolve_mutation(cls, root, info, name, username):
        user_id = info.context.user.id

        if User.nodes.filter(username__iexact=username).exclude(uid=user_id).exists():
            errors = {
                "detail": "User with username already exists"
            }  # TODO: proper error handling
            return cls(success=False, errors=errors)

        user = User.nodes.get(uid=user_id)
        user.name = name
        user.username = name
        user.save()
        return cls(success=True, user=user)
