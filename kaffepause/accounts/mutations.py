import logging

import graphene
from django.contrib.auth import get_user_model
from graphql import GraphQLError
from graphql_auth import mutations
from neomodel import NeomodelException

from kaffepause.accounts.exceptions import AccountCreationFailed
from kaffepause.accounts.services import connect_user_and_account, validate_user
from kaffepause.users.forms import UserCreationForm
from kaffepause.users.models import User

logger = logging.getLogger(__name__)

Account = get_user_model()


class Register(mutations.Register):
    """
    Register a user with an account and a related user node.
    The process is absolute, either everything is completed or nothing is.
    """

    class Arguments:
        name = graphene.String(required=True)

    @classmethod
    def mutate(cls, root, info, name, **input):
        """
        Check if the user object is valid before creating the account
        and eventually creating the user if that was successful.
        """
        user = validate_user(name=name)
        registration = super().resolve_mutation(root, info, **input)

        if registration.success:
            connect_user_and_account(user, **input)

        return registration


class DeleteAccount(mutations.DeleteAccount):
    """Permanently delete an account and the related user node."""

    @classmethod
    def mutate(cls, root, info, **input):
        account_id = info.context.user.id
        deletion = super().resolve_mutation(root, info, **input)

        if deletion.success:
            User.nodes.get(uuid=account_id).delete()
            logger.debug(f"Successfully deleted account and user (id/uuid:{account_id}")

        return deletion
