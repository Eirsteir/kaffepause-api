import graphene
from django.contrib.auth import get_user_model
from graphql_auth import mutations
from neomodel import NeomodelException

from kaffepause.common.constants import Messages
from kaffepause.users.models import User

Account = get_user_model()


class Register(mutations.Register):
    """Consistently create an account and a related user node. Update the new user with given name."""

    class Arguments:
        name = graphene.String(required=True)

    @classmethod
    def mutate(cls, root, info, name, **input):
        registration = cls.resolve_mutation(root, info, **input)
        if registration.success:
            email = input.get(Account.EMAIL_FIELD, False)
            account = Account.objects.get(email=email)
            user = User(uid=account.id, **account)
            try:
                user.save()
            except NeomodelException:
                account.delete()
                return cls(success=False, errors=Messages.ACCOUNT_CREATION_FAILED)

            user.name = name
            user.save()

        return registration


class DeleteAccount(mutations.DeleteAccount):
    """Consistently delete an account and the related user node."""

    @classmethod
    def mutatate(cls, root, info, **input):
        deletion = cls.resolve_mutation(root, info, **input)
        if deletion.success:
            account = info.context.user
            try:
                user = User.nodes.get(uid=account.id)
            except User.DoesNotExist:
                return deletion
            user.delete()

        return deletion
