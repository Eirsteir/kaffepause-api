from django.core.exceptions import ValidationError


class InvalidFriendshipDeletion(ValidationError):
    pass


class InvalidFriendshipStatusChange(ValidationError):
    pass


class UnnecessaryStatusUpdate(ValidationError):
    pass
