from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from graphql_auth.models import UserStatus

from kaffepause.friendships.admin import FriendshipInline
from kaffepause.users.forms import UserChangeForm, UserCreationForm

User = get_user_model()


class UserStatusInline(admin.TabularInline):
    model = UserStatus


class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    list_display = ["email", "is_superuser"]
    search_fields = ["email", "id"]
    ordering = ("email",)
    inlines = (
        UserStatusInline,
        FriendshipInline,
    )


admin.site.register(User, UserAdmin)
