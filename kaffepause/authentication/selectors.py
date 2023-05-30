from datetime import datetime
from typing import Optional

from kaffepause.accounts.models import Session, Account
from kaffepause.authentication.exceptions import PermissionDenied
from kaffepause.users import models


def get_user_by_session_token(session_token: str) -> Optional[models.User]:
    """
    Return the user associated with a session token from a valid session.
    """
    session = Session.nodes.get_or_none(session_token=session_token)

    if session is None:
        return None

    if session.expires < datetime.utcnow():
        raise PermissionDenied("Session expired")  # TODO: return None instead?

    return session.user.single()


def get_user_by_email(email: str) -> Optional[models.User]: # TODO: session expiration?
    """
    Return the user associated with an email address
    """
    user = models.User.nodes.get_or_none(email=email)

    return user


def get_user_by_social_id(provider: str, access_token: str) -> Optional[models.User]:
    """
    Return the user associated with a social provider and access token.
    """
    account = Account.nodes.get_or_none(provider=provider, access_token=access_token)

    if account is None:
        return None

    if account.expires < datetime.utcnow():
        raise PermissionDenied("Session expired")  # TODO: return None instead?

    return account.user.single()
