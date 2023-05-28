from functools import wraps

from graphql_jwt.decorators import context
from graphql_jwt.decorators import login_required as gql_login_required


def login_required(method):
    """Require user to be logged in and set current user on the class ref."""

    @gql_login_required
    @wraps(method)
    @context(method)
    def wrapper(context, ref, *args, **kwargs):
        # ref._user = context.user
        return method(ref, *args, **kwargs)

    return wrapper
