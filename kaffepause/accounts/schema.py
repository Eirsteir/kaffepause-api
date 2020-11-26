import graphene
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.transaction import atomic
from graphene import relay
from graphene_django import DjangoConnectionField
from graphql_auth import mutations

from kaffepause.accounts.models import Account
from kaffepause.users.models import User
from kaffepause.users.types import UserType

UserModel = get_user_model()


class Register(mutations.Register):
    class Arguments:
        name = graphene.String(required=True)

    @classmethod
    def mutate(cls, root, info, name, **input):
        # TODO: fix this flow, should revert account creation when user is not found or fails
        with transaction.atomic:
            registration = cls.resolve_mutation(root, info, **input)
            email = input.get(UserModel.EMAIL_FIELD, False)
            account = Account.objects.get(email=email)

            user = User.nodes.get(uid=account.id)
            user.name = name
            user.save()
        return registration


class AuthMutation(graphene.ObjectType):
    register = Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    resend_activation_email = mutations.ResendActivationEmail.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()
    password_set = mutations.PasswordSet.Field()  # For passwordless registration
    password_change = mutations.PasswordChange.Field()
    archive_account = mutations.ArchiveAccount.Field()
    delete_account = mutations.DeleteAccount.Field()
    send_secondary_email_activation = mutations.SendSecondaryEmailActivation.Field()
    verify_secondary_email = mutations.VerifySecondaryEmail.Field()
    swap_emails = mutations.SwapEmails.Field()
    remove_secondary_email = mutations.RemoveSecondaryEmail.Field()

    # django-graphql-jwt inheritances
    token_auth = mutations.ObtainJSONWebToken.Field()
    verify_token = mutations.VerifyToken.Field()
    refresh_token = mutations.RefreshToken.Field()
    revoke_token = mutations.RevokeToken.Field()


class AccountQuery(graphene.ObjectType):

    account = relay.Node.Field(UserType)

    def resolve_account(self, info):
        user_account = info.context.user
        if user_account.is_authenticated:
            return user_account
        return None


class Query(AccountQuery, graphene.ObjectType):
    pass


class Mutation(AuthMutation, graphene.ObjectType):
    pass
