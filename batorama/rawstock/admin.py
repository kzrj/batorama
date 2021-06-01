from django.contrib import admin

from rawstock.models import Timber, TimberRecord


@admin.register(Timber)
class TimberAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Timber._meta.fields]


@admin.register(TimberRecord)
class TimberRecordAdmin(admin.ModelAdmin):
    list_display = [f.name for f in TimberRecord._meta.fields]
