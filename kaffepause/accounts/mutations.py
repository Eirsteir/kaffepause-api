import logging

import graphene
from django.contrib.auth import get_user_model
from graphql_auth import mutations
from neomodel import NeomodelException

from kaffepause.common.constants import Messages
from kaffepause.users.models import User

logger = logging.getLogger(__name__)

Account = get_user_model()


class Register(mutations.Register):
    """
    Register a user with an account and a related user node.
    The given name is set on the created user node.
    If the user creation fails, the account is deleted.
    """

    class Arguments:
        name = graphene.String(required=True)

    @classmethod
    def mutate(cls, root, info, name, **input):
        # TODO: This will still send an email even if the creation fails - how about doing it the other way? or sending email manually
        registration = super().resolve_mutation(root, info, **input)
        if registration.success:
            email = input.get(Account.EMAIL_FIELD)
            account = Account.objects.get(email=email)
            try:
                User(uuid=account.id, name=name).save()
            except NeomodelException as e:
                logger.error(
                    f"Failed to create user node, deleting account (id:{account.id})",
                    exc_info=e,
                )
                account.delete()  # TODO: research best practice here
                return cls(success=False, errors=Messages.ACCOUNT_CREATION_FAILED)

            logger.debug(
                f"Successfully created new account and user node (id/uuid:{account.id})"
            )

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
