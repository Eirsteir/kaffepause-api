from django.utils.translation import gettext as _


class Messages:
    ACCOUNT_CREATION_FAILED = [
        {
            "message": _("Failed to create account. Try again later or contact us!"),
            "code": "account_creation_failed",
        }
    ]
    USERNAME_IN_USE = [
        {"message": _("A user with that username already exists."), "code": "unique"}
    ]
