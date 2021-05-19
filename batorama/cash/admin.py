from django.contrib import admin

from cash.models import CashRecord


@admin.register(CashRecord)
class CashRecordAdmin(admin.ModelAdmin):
    list_display = [f.name for f in CashRecord._meta.fields]
