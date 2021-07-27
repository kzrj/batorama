# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Q, Subquery, OuterRef, Count, Prefetch, F, Sum
from django.contrib.auth.models import User
from django.utils import timezone

from core.models import CoreModel, CoreModelManager


class AccountQuerySet(models.QuerySet):
    pass


class Account(CoreModel):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="account")
    nickname = models.CharField(max_length=20, null=True, blank=True)

    rama = models.ForeignKey('stock.Rama', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='accounts')

    is_ramshik = models.BooleanField(default=False)
    is_senior_ramshik = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    is_kladman = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    is_boss = models.BooleanField(default=False)
    is_capo = models.BooleanField(default=False)

    can_see_rama_stock = models.ManyToManyField('stock.Rama',  blank=True,
        related_name='accounts_can_see_stock')
    can_see_rama_shift = models.ManyToManyField('stock.Rama',  blank=True,
        related_name='accounts_can_see_shift')
    can_see_rama_sales = models.ManyToManyField('stock.Rama', blank=True,
        related_name='accounts_can_see_sales')
    can_see_rama_cash = models.ManyToManyField('stock.Rama', blank=True,
        related_name='accounts_can_see_cash')
    can_see_rama_daily_cash_report = models.ManyToManyField('stock.Rama', blank=True,
        related_name='accounts_can_see_rama_daily_cash_report')
    can_see_rama_resaws = models.ManyToManyField('stock.Rama', blank=True,
        related_name='accounts_can_see_resaws')
    can_see_rama_raw_stock = models.ManyToManyField('stock.Rama', blank=True,
        related_name='accounts_can_see_raw_stock')
    can_see_rama_quotas = models.ManyToManyField('stock.Rama', blank=True,
        related_name='accounts_can_see_quotas')

    cash = models.IntegerField(default=0)

    objects = AccountQuerySet.as_manager()

    def __str__(self):
        if self.user:
            return self.user.username
        return self.nickname

    def add_cash(self, amount):
        self.cash += amount
        self.save()

    def remove_cash(self, amount):
        self.cash -= amount
        self.save()