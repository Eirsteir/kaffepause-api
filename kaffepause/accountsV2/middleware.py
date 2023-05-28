
__all__ = [
    'SessionTokenMiddleware',
]

from django.contrib.auth import authenticate
from graphql_jwt.utils import get_http_authorization


def get_token_argument(request, **kwargs):

    input_fields = kwargs.get('input')
    if isinstance(input_fields, dict):
        kwargs = input_fields
    print(input_fields)

    return kwargs.get("sessionToken", None)

def _authenticate(request):
    is_anonymous = not hasattr(request, 'user') or request.user.is_anonymous
    return is_anonymous and get_http_authorization(request) is not None

class SessionTokenMiddleware:

    def resolve(self, next, root, info, **kwargs):
        print("RESOLVING IN MIDDLEWARE", next, root, info, kwargs)
        context = info.context
        print("CONTEXT: ", context)
        token_argument = get_token_argument(context, **kwargs)
        print("TOKEN: ", token_argument)

        # if jwt_settings.JWT_ALLOW_ARGUMENT and token_argument is None:
        #     user = self.cached_authentication.parent(info.path)
        #
        #     if user is not None:
        #         context.user = user
        #
        #     elif hasattr(context, 'user'):
        #         if hasattr(context, 'session'):
        #             context.user = get_user(context)
        #         else:
        #             context.user = AnonymousUser()
        #
        if _authenticate(context) or token_argument is not None:

            user = authenticate(request=context, **kwargs)

            if user is not None:
                context.user = user

                # if jwt_settings.JWT_ALLOW_ARGUMENT:
                #     self.cached_authentication.insert(info.path, user)

        return next(root, info, **kwargs)
