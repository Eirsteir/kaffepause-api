import graphene
from django.contrib.auth import get_user_model
from graphql_auth import mutations
from graphql_auth.schema import MeQuery, UserNode, UserQuery

from kaffepause.common.schema import UUIDNode
from kaffepause.friendships.selectors import get_friends

User = get_user_model()


# class ExtendedUserNode(UserNode):
#     class Meta:
#         model = User
# fields = UserNode.Meta.fields (
#     "id",
#     "name",
#     "username",
#     "friends",
# )
# filter_fields = UserNode.Meta.filter_fields + {
#     "username": ["exact", "icontains", "istartswith"],
#     "friends": ["exact"],
#     "friends__name": ["exact"],
# }
# interfaces = (UUIDNode,)

# profile_action = graphene.Field(ProfileAction)

# TODO: enable when adding login required
# friendship_status = graphene.String()
#
# def resolve_friendship_status(parent, info):
#     current_user = info.context.to_user
#     return get_friendship_status(to_user=current_user, to_user=parent)

# def resolve_friends(parent, info):
#
#     return get_friends(parent)


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


class Query(UserQuery, MeQuery, graphene.ObjectType):
    pass


class Mutation(AuthMutation, graphene.ObjectType):
    pass
