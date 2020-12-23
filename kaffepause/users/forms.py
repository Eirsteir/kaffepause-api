from django.db import models
from django.forms import ModelForm

from kaffepause.users.models import User


class UserCreationForm(ModelForm):
    name = models.CharField(max_length=100)

    class Meta:
        model = User
        fields = ("name",)
