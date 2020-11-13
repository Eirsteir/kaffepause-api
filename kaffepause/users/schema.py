import graphene
from django.contrib.auth import get_user_model
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from graphql_auth import mutations
from graphql_auth.bases import OutputErrorType
from graphql_auth.schema import UserNode
from graphql_auth.settings import graphql_auth_settings

from kaffepause.common.schema import CountingNodeConnection, UUIDNode
from kaffepause.friendships.selectors import get_friends, get_friendship_status


class User(UserNode):
    class Meta:
        model = get_user_model()
        filter_fields = graphql_auth_settings.USER_NODE_FILTER_FIELDS
        exclude = graphql_auth_settings.USER_NODE_EXCLUDE_FIELDS
        interfaces = (UUIDNode,)
        connection_class = CountingNodeConnection

    success = graphene.Boolean(default_value=True)
    errors = graphene.Field(OutputErrorType)
    friends_count = graphene.List(UserNode)

    # profile_action = graphene.Field(ProfileAction)

    friendship_status = graphene.String()
    # social_context = graphene.Field(SocialContext)

    def resolve_friendship_status(parent, info):
        current_user = info.context.user
        status = get_friendship_status(actor=current_user, user=parent)
        return status.name

    def resolve_friends_count(parent, info):

        return get_friends(parent).count()


class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    resend_activation_email = mutations.ResendActivationEmail.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()
    password_set = mutations.PasswordSet.Field()  # For passwordless registration
    password_change = mutations.PasswordChange.Field()
    update_account = mutations.UpdateAccount.Field()
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


class UserQuery(graphene.ObjectType):

    user = relay.Node.Field(User)
    users = DjangoFilterConnectionField(User)


class MeQuery(graphene.ObjectType):
    me = graphene.Field(User)

    def resolve_me(self, info):
        user = info.context.user
        if user.is_authenticated:
            return user
        return None


class Query(UserQuery, MeQuery, graphene.ObjectType):
    pass


class Mutation(AuthMutation, graphene.ObjectType):
    pass
