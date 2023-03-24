import logging

from graphql import GraphQLError
from neomodel import NeomodelException

from kaffepause.accounts.exceptions import AccountCreationFailed
from kaffepause.accounts.models import Account
from kaffepause.location.selectors import get_location
from kaffepause.users.forms import UserCreationForm

logger = logging.getLogger(__name__)


def validate_user(**kwargs):
    """Prepare the user object for creation and account connection."""
    form = UserCreationForm(kwargs)
    if form.is_valid():
        return form.save(commit=False)
    
    raise GraphQLError(form.errors.get_json_data())


def create_user(user, preferred_location_uuid=None, **kwargs):
    connect_user_and_account(user, **kwargs)
    if preferred_location_uuid:
        connect_preferred_location(preferred_location_uuid, user)
    return user


def connect_preferred_location(preferred_location_uuid, user):
    preferred_location = get_location(location_uuid=preferred_location_uuid)
    user.preferred_location.connect(preferred_location)


def connect_user_and_account(user, **kwargs):
    email = kwargs.get(Account.EMAIL_FIELD)
    account = Account.objects.get(email=email)
    user.uuid = account.id
    try_to_create_user(account, user)


def try_to_create_user(account, user):
    """Try to save the user and delete the account upon failure."""
    try:
        user.save()
    except NeomodelException:
        logger.exception(
            f"Failed to create user node, deleting account (id:{account.id})",
        )
        account.delete()
        raise AccountCreationFailed
    logger.debug(
        f"Successfully created new account and user node (id/uuid:{account.id})"
    )
