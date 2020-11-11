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
    add_form = UserCreationForm
    fieldsets = (("User", {"fields": ("name",)}),) + tuple(
        auth_admin.UserAdmin.fieldsets
    )
    list_display = ["username", "name", "is_superuser"]
    search_fields = ["name", "username", "first_name", "last_name"]
    inlines = (
        UserStatusInline,
        FriendshipInline,
    )


admin.site.register(User, UserAdmin)
