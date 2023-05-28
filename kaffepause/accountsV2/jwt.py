import logging

from graphql_jwt.settings import jwt_settings
from graphql_jwt.utils import jwt_payload as graphql_jwt_payload

from kaffepause.users.models import User

logger = logging.getLogger(__name__)


def get_user_by_natural_key(username):

    logger.debug(f"Auth: getting user by naturalkey: {username}")

    try:
        return User.nodes.get(email=username)
    except User.DoesNotExist as e:
        logger.error(f"Auth: User not found : {username}", exc_info=e)
        return None


def jwt_payload(user, context=None):
    payload = graphql_jwt_payload(user, context)
    payload["user_id"] = str(user.id)
    return payload


def get_username_from_user(payload):
    # return payload.get(get_user_model().USERNAME_FIELD)
    return payload.get(User.USERNAME_FIELD) # Email?

import json
from typing import Any
from Crypto.Protocol.KDF import HKDF
from Crypto.Hash import SHA256
from jose import jwe


def getDerivedEncryptionKey(secret: str) -> Any:
    # Think about including the context in your environment variables.
    context = str.encode("NextAuth.js Generated Encryption Key")
    return HKDF(
        master=secret.encode(),
        key_len=32,
        salt="".encode(),
        hashmod=SHA256,
        num_keys=1,
        context=context,
    )


def get_token(token: str, context=None):
    '''
    Get the JWE payload from a NextAuth.js JWT/JWE token in Python

    Steps:
    1. Get the encryption key using HKDF defined in RFC5869
    2. Decrypt the JWE token using the encryption key
    3. Create a JSON object from the decrypted JWE token
    '''
    # Retrieve the same JWT_SECRET which was used to encrypt the JWE token on the NextAuth Server
    jwt_secret = jwt_settings.JWT_SECRET_KEY
    encryption_key = getDerivedEncryptionKey(jwt_secret)
    payload_str = jwe.decrypt(token, encryption_key).decode()
    payload: dict[str, Any] = json.loads(payload_str)

    return payload
