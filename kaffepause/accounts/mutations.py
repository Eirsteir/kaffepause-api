import logging

import graphene
from django.contrib.auth import get_user_model
from graphql import GraphQLError
from graphql_auth import mutations
from neomodel import NeomodelException

from kaffepause.accounts.exceptions import AccountCreationFailed
from kaffepause.common.constants import Messages
from kaffepause.users.forms import UserCreationForm
from kaffepause.users.models import User

logger = logging.getLogger(__name__)

Account = get_user_model()


class Register(mutations.Register):
    """
    Register a user with an account and a related user node.
    The process is absolute, either everything is completed or nothing is.
    """

    node_form = UserCreationForm

    class Arguments:
        name = graphene.String(required=True)

    @classmethod
    def mutate(cls, root, info, name, **input):
        """
        Check if the user object is valid before creating the account
        and eventually creating the user if that was successful.
        """
        user = cls.__validate_user_or_raise(name=name)

        # TODO: This will still send an email even if the creation fails - how about doing it the other way? or
        #  sending email manually
        registration = super().resolve_mutation(root, info, **input)

        if registration.success:
            cls.__perform_connected_user_creation(user, **input)

        print(user)
        return registration

    @classmethod
    def __validate_user_or_raise(cls, **kwargs):
        form = cls.node_form(kwargs)
        if form.is_valid():
            return form.save(commit=False)
        print("HERE")
        raise GraphQLError(form.errors.get_json_data())

    @classmethod
    def __perform_connected_user_creation(cls, user, **kwargs):
        email = kwargs.get(Account.EMAIL_FIELD)
        account = Account.objects.get(email=email)
        user.uuid = account.id
        cls.__try_to_save_user(account, user)

    @classmethod
    def __try_to_save_user(cls, account, user):
        """Try to save the user and delete the account if upon failure."""
        try:
            user.save()
        except NeomodelException as e:
            logger.error(
                f"Failed to create user node, deleting account (id:{account.id})",
                exc_info=e,
            )
            account.delete()
            raise AccountCreationFailed
        logger.debug(
            f"Successfully created new account and user node (id/uuid:{account.id})"
        )


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
