from django.contrib import admin

from accounts.models import (Account, CashRecord)


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Account._meta.fields]


@admin.register(CashRecord)
class CashRecordAdmin(admin.ModelAdmin):
    list_display = [f.name for f in CashRecord._meta.fields]
