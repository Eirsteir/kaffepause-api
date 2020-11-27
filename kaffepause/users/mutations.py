import graphene

from kaffepause.common.bases import Mutation
from kaffepause.common.constants import Messages
from kaffepause.users.models import User
from kaffepause.users.types import UserType


class UpdateProfile(Mutation):
    class Arguments:
        name = graphene.String(required=True)
        username = graphene.String(required=True)

    user = graphene.Field(UserType)

    @classmethod
    def resolve_mutation(cls, root, info, name, username):
        account = info.context.user

        if (
            User.nodes.filter(username__iexact=username)
            .exclude(uid=account.id)
            .exists()
        ):
            return cls(success=False, errors=Messages.USERNAME_IN_USE)

        user = User.nodes.get_or_create(uid=account.id, **account)
        user.name = name
        user.username = name
        user.save()
        return cls(success=True, user=user)
