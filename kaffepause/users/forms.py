from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from kaffepause.users.models import User


class UserCreationForm(forms.ModelForm):
    name = models.CharField(max_length=100)

    class Meta:
        model = User
        fields = ("name",)


class UserUpdateForm(forms.ModelForm):
    name = forms.CharField(max_length=100, required=False)
    username = forms.CharField(max_length=100, required=False)
    # profile_pic = forms.URLField(required=False)

    error_message = {"duplicate_username": _("This username has already been taken.")}

    class Meta:
        model = User
        fields = (
            "name",
            "username",
            "locale",
            "profile_pic",
        )

    def clean_username(self):
        username = self.cleaned_data["username"]

        try:
            User.nodes.get(username=username)
        except User.DoesNotExist:
            return username

        raise ValidationError(self.error_message["duplicate_username"])
