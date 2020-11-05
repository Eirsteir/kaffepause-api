from django.contrib import admin

from .forms import RelationshipStatusAdminForm
from .models import Friendship, RelationshipStatus


class FriendshipInline(admin.StackedInline):
    model = Friendship
    fk_name = "requester"


@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    search_fields = ("requester__username", "addressee__username")
    list_display = (
        "requester",
        "addressee",
        "status",
    )


@admin.register(RelationshipStatus)
class RelationshipStatusAdmin(admin.ModelAdmin):
    form = RelationshipStatusAdminForm
