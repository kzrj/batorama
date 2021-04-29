from django.contrib import admin

from stock.models import (Lumber, Shift, LumberRecord, Sale)


@admin.register(Lumber)
class LumberAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Lumber._meta.fields]


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Shift._meta.fields]


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Sale._meta.fields]


@admin.register(LumberRecord)
class LumberRecordAdmin(admin.ModelAdmin):
    list_display = [f.name for f in LumberRecord._meta.fields]