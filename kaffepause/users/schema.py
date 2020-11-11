import graphene
from django.contrib.auth import get_user_model
from graphene_django.filter import DjangoFilterConnectionField
from graphql_auth import mutations
from graphql_auth.bases import OutputErrorType
from graphql_auth.schema import UserNode
from graphql_auth.settings import graphql_auth_settings

from kaffepause.common.schema import UUIDNode
from kaffepause.friendships.selectors import get_friends, get_friendship_status

User = get_user_model()


class ExtendedUserNode(UserNode):
    class Meta:
        model = User
        filter_fields = graphql_auth_settings.USER_NODE_FILTER_FIELDS
        exclude = graphql_auth_settings.USER_NODE_EXCLUDE_FIELDS
        interfaces = (UUIDNode,)

    success = graphene.Boolean(default_value=True)
    errors = graphene.Field(OutputErrorType)
    friends = graphene.List(UserNode)

    # profile_action = graphene.Field(ProfileAction)

    # TODO: enable when adding login required
    friendship_status = graphene.String()

    def resolve_friendship_status(parent, info):
        current_user = info.context.to_user
        return get_friendship_status(actor=current_user, user=parent)

    def resolve_friends(parent, info):

        return get_friends(parent)


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
    user = graphene.relay.Node.Field(ExtendedUserNode)
    users = DjangoFilterConnectionField(ExtendedUserNode)


class MeQuery(graphene.ObjectType):
    me = graphene.Field(ExtendedUserNode)

    def resolve_me(self, info):
        user = info.context.user
        if user.is_authenticated:
            return user
        return None


class Query(UserQuery, MeQuery, graphene.ObjectType):
    pass


class Mutation(AuthMutation, graphene.ObjectType):
    pass
