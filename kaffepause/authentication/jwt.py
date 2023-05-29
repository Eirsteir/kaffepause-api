import logging
from datetime import datetime

import jwt
from django.conf import settings

from django.utils.translation import gettext as _
import json
from typing import Any
from Crypto.Protocol.KDF import HKDF
from Crypto.Hash import SHA256
from jose import jwe, jwt


from kaffepause.users.models import User

logger = logging.getLogger(__name__)


def get_user_by_natural_key(email):

    logger.debug(f"Auth: getting user by natural key: {email}")

    try:
        return User.nodes.get(email=email)
    except User.DoesNotExist as e:
        logger.error(f"Auth: User not found : {email}", exc_info=e)
        return None


def jwt_payload(user, context=None):
    username = user.get_username()

    if hasattr(username, 'pk'):
        username = username.pk

    payload = {user.USERNAME_FIELD: username, 'exp': datetime.utcnow() + settings.JWT_EXPIRATION_DELTA,
               "user_id": str(user.id)}

    # if jwt_settings.JWT_ALLOW_REFRESH:
    #     payload['origIat'] = timegm(datetime.utcnow().utctimetuple())

    return payload


def get_username_from_user(payload):
    # return payload.get(get_user_model().USERNAME_FIELD)
    return payload.get(User.USERNAME_FIELD) # Email?


def get_http_authorization(request):
    auth = request.META.get(settings.JWT_AUTH_HEADER_NAME, '').split()
    prefix = settings.JWT_AUTH_HEADER_PREFIX

    if len(auth) != 2 or auth[0].lower() != prefix.lower():
        return request.COOKIES.get(settings.JWT_COOKIE_NAME)
    return auth[1]


def get_credentials(request, **kwargs):
    return get_http_authorization(request)


def get_user_by_token(token, context=None):
    payload = get_payload(token, context)
    return get_user_by_payload(payload)


# TODO: update with correct package: jose
def get_payload(token, context=None):
    try:
        payload = decode_jwt(token, context)
    except jwe.JWEError:
        raise jwt.JWTError('Error decoding token')
    return payload


def get_user_by_payload(payload):
    email = get_username_from_user(payload)

    if not email:
        raise jwt.JWTError('Invalid payload')

    user = get_user_by_natural_key(email)

    if user is not None and not user.is_active:
        raise jwt.JWTError('User is disabled')
    return user


def get_derived_encryption_key(secret: str) -> Any:
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


def decode_jwt(token: str, context=None):
    '''
    Get the JWE payload from a NextAuth.js JWT/JWE token in Python

    Steps:
    1. Get the encryption key using HKDF defined in RFC5869
    2. Decrypt the JWE token using the encryption key
    3. Create a JSON object from the decrypted JWE token
    '''
    # Retrieve the same JWT_SECRET which was used to encrypt the JWE token on the NextAuth Server
    jwt_secret = settings.JWT_SECRET_KEY
    encryption_key = get_derived_encryption_key(jwt_secret)
    payload_str = jwe.decrypt(token, encryption_key).decode()
    payload: dict[str, Any] = json.loads(payload_str)

    return payload

