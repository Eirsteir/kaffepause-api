from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from graphql_auth.models import UserStatus

from kaffepause.accounts.forms import AccountChangeForm

Account = get_user_model()


class AccountStatusInline(admin.TabularInline):
    model = UserStatus


class AccountAdmin(auth_admin.UserAdmin):

    form = AccountChangeForm
    list_display = ["email", "is_superuser"]
    search_fields = ["email", "id"]
    ordering = ("email",)
    inlines = (AccountStatusInline,)


admin.site.register(Account, AccountAdmin)
