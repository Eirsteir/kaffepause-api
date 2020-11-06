from django.contrib import admin

from .forms import RelationshipStatusAdminForm
from .models import Relationship, RelationshipStatus


class FriendshipInline(admin.StackedInline):
    model = Relationship
    fk_name = "from_user"


@admin.register(Relationship)
class FriendshipAdmin(admin.ModelAdmin):
    search_fields = ("from_user__username", "to_user__username")


@admin.register(RelationshipStatus)
class RelationshipStatusAdmin(admin.ModelAdmin):
    form = RelationshipStatusAdminForm
