import logging
from abc import ABC, abstractmethod

from kaffepause.users.exceptions import UserDoesNotExist
from kaffepause.users.models import User
from kaffepause.users.selectors import get_user_from_account

logger = logging.getLogger(__name__)


class SocialProvider(ABC):
    @abstractmethod
    def do_create_user(self, account, response):
        """The account can be assumed to be verified when it comes from a social authentication provider."""
        account.verify()
        try:
            return get_user_from_account(account=account)
        except UserDoesNotExist:
            logger.debug(
                f"Registering new user from {self.__class__.__name__} (id: {account.id})"
            )
            return User(uuid=account.id)


class FacebookAuthProvider(SocialProvider):
    def do_create_user(self, account, response):
        user = super().do_create_user(account, response)

        user.name = response.get("name")
        user.profile_pic = response.get("picture").get("data").get("url")
        user.save()


class GoogleOAuth2Provider(SocialProvider):
    def do_create_user(self, account, response):
        user = super().do_create_user(account, response)

        user.name = response.get("name")
        user.locale = response.get("locale")
        user.profile_pic = response.get("picture")
        user.save()


class ProviderNotFound(Exception):
    pass


class SocialAuthProviderFactory:
    providers = {
        "facebook": FacebookAuthProvider,
        "google-oauth2": GoogleOAuth2Provider,
    }

    @classmethod
    def get_provider(cls, provider_name):
        try:
            return cls.providers[provider_name]()
        except KeyError:
            raise ProviderNotFound(f"Provider not found: {provider_name})")


def create_user(backend, user, response, *args, **kwargs):
    """Only create a new User if the Account is new."""
    if kwargs.get("is_new"):
        __create_new_user(backend, response, user)


def __create_new_user(backend, response, user):
    try:
        provider = SocialAuthProviderFactory.get_provider(backend.name)
    except ProviderNotFound as e:
        logger.exception(e)
        return

    provider.do_create_user(account=user, response=response)
    logger.debug(f"Successfully created new account and user node (id/uuid:{user.id})")
