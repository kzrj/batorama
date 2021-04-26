from django.contrib import admin

from quotas.models import (Quota, RoundLumberIncome)


@admin.register(Quota)
class QuotaAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Quota._meta.fields]


@admin.register(RoundLumberIncome)
class RoundLumberIncomeAdmin(admin.ModelAdmin):
    list_display = [f.name for f in RoundLumberIncome._meta.fields]