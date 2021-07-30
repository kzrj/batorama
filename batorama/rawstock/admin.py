from django.contrib import admin

from rawstock.models import Timber, TimberRecord, IncomeTimber, Quota


@admin.register(Timber)
class TimberAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Timber._meta.fields]


@admin.register(TimberRecord)
class TimberRecordAdmin(admin.ModelAdmin):
    list_display = [f.name for f in TimberRecord._meta.fields]


@admin.register(Quota)
class QuotaAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Quota._meta.fields]


@admin.register(IncomeTimber)
class IncomeTimberAdmin(admin.ModelAdmin):
    list_display = [f.name for f in IncomeTimber._meta.fields]