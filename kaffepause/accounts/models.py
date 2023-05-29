#
# #------------------------------------------------------------
# import uuid
# from django.contrib.auth.base_user import BaseUserManager
# from django.contrib.auth.models import AbstractUser
# from django.db import models
# from django.utils.translation import gettext_lazy as _
#
# class AccountManager(BaseUserManager):
#     use_in_migrations = True
#
#     def _create_user(self, email, password, **extra_fields):
#         """
#         Create and save a user with the given username, email, and password.
#         """
#         if not email:
#             raise ValueError("The given email must be set")
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_user(self, email, password=None, **extra_fields):
#         extra_fields.setdefault("is_staff", False)
#         extra_fields.setdefault("is_superuser", False)
#         return self._create_user(email, password, **extra_fields)
#
#     def create_superuser(self, email, password, **extra_fields):
#         extra_fields.setdefault("is_staff", True)
#         extra_fields.setdefault("is_superuser", True)
#
#         if extra_fields.get("is_staff") is not True:
#             raise ValueError("Superuser must have is_staff=True.")
#         if extra_fields.get("is_superuser") is not True:
#             raise ValueError("Superuser must have is_superuser=True.")
#
#         return self._create_user(email, password, **extra_fields)
#
#
# class AccountOld(AbstractUser):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     email = models.EmailField(_("email address"), unique=True)
#
#     username = None
#     first_name = None
#     last_name = None
#
#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = []
#
#     objects = AccountManager()
#
#     def __str__(self):
#         return self.email
#
#     def verify(self):
#         user_status = self.status
#         if not user_status.verified:
#             user_status.verified = True
#             user_status.save(update_fields=["verified"])


#------------------------------------------------------------


from neomodel import (StructuredNode, StringProperty, IntegerProperty,
                      DateTimeProperty, RelationshipFrom, UniqueIdProperty)

from kaffepause.authentication.enums import AccountRelationship
from kaffepause.common.enums import USER


class Account(StructuredNode):
    uuid = UniqueIdProperty(db_property="id")  # Neomodel overrides field id
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
    uuid = UniqueIdProperty(db_property="id")  # Neomodel overrides field id
    sessionToken = StringProperty(unique_index=True, required=True)
    userId = StringProperty(required=True)
    expires = DateTimeProperty()
    user = RelationshipFrom(USER, AccountRelationship.HAS_SESSION)


class VerificationToken(StructuredNode):
    identifier = StringProperty()
    token = StringProperty(unique_index=True, required=True)
    expires = DateTimeProperty()

