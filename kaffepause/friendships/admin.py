from django.contrib import admin

from .models import Friendship

admin.register(Friendship)


@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    fields = ["requester", "addressee", "status"]
    search_fields = ["requester", "addressee"]
