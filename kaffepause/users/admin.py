from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

from kaffepause.relationships.admin import FriendshipInline
from kaffepause.users.forms import UserChangeForm, UserCreationForm

User = get_user_model()


class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (("User", {"fields": ("name",)}),) + tuple(
        auth_admin.UserAdmin.fieldsets
    )
    list_display = ["username", "name", "is_superuser"]
    search_fields = ["name"]
    inlines = (FriendshipInline,)


admin.site.register(User, UserAdmin)
