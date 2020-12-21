import logging
from typing import Iterable
from uuid import UUID

from neomodel import Q

from kaffepause.accounts.models import Account
from kaffepause.users.exceptions import UserDoesNotExist
from kaffepause.users.models import User

logger = logging.getLogger(__name__)


def get_user_from_account(account: Account) -> User:
    return get_user(user_uuid=account.id)


def get_user(*, user_uuid: UUID) -> User:
    try:
        return User.nodes.get(uuid=user_uuid)
    except User.DoesNotExist as e:
        logger.debug(f"Could not find user with uuid: {user_uuid}", exc_info=e)
        raise UserDoesNotExist


def search_users(*, query: str, searched_by: User) -> Iterable[User]:
    search_query = Q(name__icontains=query) | Q(username__icontains=query)

    return User.nodes.filter(search_query).exclude(uuid=searched_by.uuid).all()


def get_users(*, fetched_by: User) -> Iterable[User]:
    return User.nodes.exclude(uuid=fetched_by.uuid).all()
