from django.contrib.auth import get_user_model
from graphql_auth.schema import UserNode
from graphql_auth.settings import graphql_auth_settings

from kaffepause.common.bases import UUIDNode


class AccountType(UserNode):
    class Meta:
        model = get_user_model()
        filter_fields = graphql_auth_settings.USER_NODE_FILTER_FIELDS
        exclude = graphql_auth_settings.USER_NODE_EXCLUDE_FIELDS
        interfaces = (UUIDNode,)
