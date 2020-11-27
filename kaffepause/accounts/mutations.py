import graphene
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from graphql_auth import mutations

from kaffepause.users.models import User

Account = get_user_model()


class Register(mutations.Register):
    class Arguments:
        name = graphene.String(required=True)

    @classmethod
    def mutate(cls, root, info, name, **input):
        registration = cls.resolve_mutation(root, info, **input)
        if registration.success:
            email = input.get(Account.EMAIL_FIELD, False)
            account = Account.objects.get(email=email)
            try:
                user = User.nodes.get(uid=account.id)
            except User.DoesNotExist:
                account.delete()
                return cls(success=False, errors={_("Failed to create account")})

            user.name = name
            user.save()

        return registration


class DeleteAccount(mutations.DeleteAccount):
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
