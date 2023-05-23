from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
                      DateTimeProperty, RelationshipTo, RelationshipFrom, UniqueIdProperty)

from kaffepause.accountsV2.enums import AccountRelationship
from kaffepause.common.enums import ACCOUNT, SESSION, USER


class Account(StructuredNode):
    id = UniqueIdProperty()
    userId = StringProperty(required=True)
    type = StringProperty(required=True)
    provider = StringProperty(required=True)
    providerAccountId = StringProperty(required=True)
    refresh_token = StringProperty()
    access_token = StringProperty()
    expires_at = IntegerProperty()
    refresh_token_expires_in = IntegerProperty()  # For github: https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/refreshing-user-access-tokens#response
    token_type = StringProperty()
    scope = StringProperty()
    id_token = StringProperty()
    session_state = StringProperty()
    user = RelationshipFrom(USER, AccountRelationship.HAS_ACCOUNT)


class Session(StructuredNode):
    id = UniqueIdProperty()
    sessionToken = StringProperty(unique_index=True, required=True)
    userId = StringProperty(required=True)
    expires = DateTimeProperty()
    user = RelationshipFrom(USER, AccountRelationship.HAS_SESSION)


class VerificationToken(StructuredNode):
    identifier = StringProperty()
    token = StringProperty(unique_index=True, required=True)
    expires = DateTimeProperty()

