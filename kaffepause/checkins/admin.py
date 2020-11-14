from django.contrib import admin

from kaffepause.checkins.models import CheckIn, CheckInStatus


@admin.register(CheckInStatus)
class StudyStatusAdmin(admin.ModelAdmin):
    pass


@admin.register(CheckIn)
class CheckInAdmin(admin.ModelAdmin):
    pass
