from django.contrib.auth import authenticate

from kaffepause.accountsV2.auth import get_http_authorization


def get_token_argument(request, **kwargs):

    input_fields = kwargs.get('input')
    if isinstance(input_fields, dict):
        kwargs = input_fields
    print(input_fields)

    return kwargs.get("sessionToken", None)


def _authenticate(request):
    is_anonymous = not hasattr(request, 'user')  # or request.user.is_anonymous
    return is_anonymous and get_http_authorization(request) is not None


class JSONWebTokenMiddleware:

    def resolve(self, next, root, info, **kwargs):
        context = info.context
        token_argument = get_token_argument(context, **kwargs)

        if _authenticate(context) or token_argument is not None:

            user = authenticate(request=context, **kwargs)

            if user is not None:
                context.user = user

        return next(root, info, **kwargs)
