from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from graphql_auth.models import UserStatus

from kaffepause.accounts.forms import AccountChangeForm

Account = get_user_model()


class AccountStatusInline(admin.TabularInline):
    model = UserStatus


class AccountAdmin(auth_admin.UserAdmin):

    form = AccountChangeForm
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["email", "is_superuser"]
    search_fields = ["email", "id"]
    ordering = ("email",)
    inlines = (AccountStatusInline,)


admin.site.register(Account, AccountAdmin)
