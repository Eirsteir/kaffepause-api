from graphql_jwt.backends import JSONWebTokenBackend
from graphql_jwt.shortcuts import get_user_by_token
from graphql_jwt.utils import get_credentials
from graphql_jwt.exceptions import JSONWebTokenError


class Neo4jGraphQLAuthBackend(JSONWebTokenBackend):

    def authenticate(self, request=None, **kwargs):
        print("authenticating")

        if request is None or getattr(request, "_jwt_token_auth", False):
            return None

        token = get_credentials(request, **kwargs)

        if token is not None:
            user = get_user_by_token(token, request)
            user.is_authenticated = True
            print(user)
            return user

        return None
