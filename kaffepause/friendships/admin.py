from django.contrib import admin

from .forms import FriendshipStatusAdminForm
from .models import Friendship, FriendshipStatus


class FriendshipInline(admin.StackedInline):
    model = Friendship
    fk_name = "from_user"


@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    search_fields = ("from_user__username", "to_user__username")


@admin.register(FriendshipStatus)
class FriendshipStatusAdmin(admin.ModelAdmin):
    form = FriendshipStatusAdminForm
