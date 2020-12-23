from kaffepause.common.constants import Messages
from kaffepause.common.exceptions import DefaultError


class AccountCreationFailed(DefaultError):
    default_message = Messages.ACCOUNT_CREATION_FAILED
