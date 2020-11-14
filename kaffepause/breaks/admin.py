from django.contrib import admin

from kaffepause.breaks.models import Break, BreakHistory, BreakInvitation


@admin.register(Break)
class BreakAdmin(admin.ModelAdmin):
    pass


@admin.register(BreakInvitation)
class BreakInvitationAdmin(admin.ModelAdmin):
    pass


@admin.register(BreakHistory)
class BreakHistoryAdmin(admin.ModelAdmin):
    pass
