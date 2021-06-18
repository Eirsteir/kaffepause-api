from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from kaffepause.users.models import User


class UserCreationForm(forms.ModelForm):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=50)

    class Meta:
        model = User
        fields = ("name", "username")


class UserUpdateForm(forms.ModelForm):
    name = forms.CharField(max_length=100, required=True)
    username = forms.CharField(max_length=100, required=True)
    locale = forms.CharField(max_length=10, required=True)

    error_message = {"duplicate_username": _("This username has already been taken.")}

    class Meta:
        model = User
        fields = (
            "name",
            "username",
            "locale",
        )

    def clean_username(self):
        username = self.cleaned_data["username"]
        if username == self.instance.username:
            return username

        try:
            User.nodes.get(username=username)
        except User.DoesNotExist:
            return username

        raise ValidationError(self.error_message["duplicate_username"])
