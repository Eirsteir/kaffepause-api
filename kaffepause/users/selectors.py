from typing import Iterable

from neomodel import Q

from kaffepause.users.models import User


def get_user_from_account(user):
    user = User.nodes.get(uuid=user.id)
    return user


def search_users(*, query: str, searched_by: User) -> Iterable[User]:
    search_query = Q(name__icontains=query) | Q(username__icontains=query)

    return User.nodes.filter(search_query).exclude(uuid=searched_by.uuid).all()


def get_users(*, fetched_by: User) -> Iterable[User]:
    return User.nodes.exclude(uuid=fetched_by.uuid).all()
