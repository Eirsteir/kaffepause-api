import graphene
import graphql_social_auth
from django.contrib.auth import get_user_model
from graphql_auth import mutations as auth_mutations
from graphql_jwt.decorators import login_required

from kaffepause.accounts import mutations
from kaffepause.accounts.types import AccountNode

Account = get_user_model()


class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    delete_account = mutations.DeleteAccount.Field()

    social_auth = graphql_social_auth.SocialAuthJWT.Field()

    # graphql-auth inheritances
    verify_account = auth_mutations.VerifyAccount.Field()
    resend_activation_email = auth_mutations.ResendActivationEmail.Field()
    send_password_reset_email = auth_mutations.SendPasswordResetEmail.Field()
    password_reset = auth_mutations.PasswordReset.Field()
    password_set = auth_mutations.PasswordSet.Field()  # For passwordless registration
    password_change = auth_mutations.PasswordChange.Field()
    archive_account = auth_mutations.ArchiveAccount.Field()
    send_secondary_email_activation = (
        auth_mutations.SendSecondaryEmailActivation.Field()
    )
    verify_secondary_email = auth_mutations.VerifySecondaryEmail.Field()
    swap_emails = auth_mutations.SwapEmails.Field()
    remove_secondary_email = auth_mutations.RemoveSecondaryEmail.Field()

    # django-graphql-jwt inheritances
    token_auth = auth_mutations.ObtainJSONWebToken.Field()
    verify_token = auth_mutations.VerifyToken.Field()
    refresh_token = auth_mutations.RefreshToken.Field()
    revoke_token = auth_mutations.RevokeToken.Field()


class AccountQuery(graphene.ObjectType):

    my_account = graphene.Field(AccountNode)

    @login_required
    def resolve_my_account(root, info):
        return info.context.user


class Query(AccountQuery, graphene.ObjectType):
    pass


class Mutation(AuthMutation, graphene.ObjectType):
    pass
