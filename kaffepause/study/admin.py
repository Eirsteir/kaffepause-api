from django.contrib import admin

from kaffepause.study.models import (
    Break,
    BreakHistory,
    BreakInvitation,
    CheckIn,
    CheckInStatus,
)


@admin.register(CheckInStatus)
class StudyStatusAdmin(admin.ModelAdmin):
    pass


@admin.register(CheckIn)
class CheckInAdmin(admin.ModelAdmin):
    pass


@admin.register(Break)
class BreakAdmin(admin.ModelAdmin):
    pass


@admin.register(BreakInvitation)
class BreakInvitationAdmin(admin.ModelAdmin):
    pass


@admin.register(BreakHistory)
class BreakHistoryAdmin(admin.ModelAdmin):
    pass
