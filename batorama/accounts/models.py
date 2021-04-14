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

    is_ramshik = models.BooleanField(default=False)
    is_senior_ramshik = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)

    cash = models.IntegerField(default=0)

    objects = AccountQuerySet.as_manager()

    def __str__(self):
        return self.user.username

    def add_cash(self, amount):
        self.cash += amount
        self.save()

    def remove_cash(self, amount):
        self.cash -= amount
        self.save()


class CashRecordQuerySet(models.QuerySet):
    def create_payout_from_shift(self, employee, shift, amount, initiator=None):
        self.create(amount=amount, account=employee, shift=shift, record_type='payout_to_employee_from_shift',
            initiator=initiator)
        employee.add_cash(amount)

    def create_withdraw_employee(self, employee, amount, initiator=None):
        self.create(amount=amount, account=employee, record_type='withdraw_employee', initiator=initiator)
        employee.remove_cash(amount)


class CashRecord(CoreModel):
    amount = models.IntegerField()
    RECORD_TYPES = [('payout_to_employee_from_shift', 'Начисление работникам'),
         ('withdraw_employee', 'Обналичивание работникам')]
    record_type = models.CharField(max_length=50, choices=RECORD_TYPES)

    account = models.ForeignKey(Account, on_delete=models.SET_NULL, related_name='cash_records',
        null=True, blank=True)

    shift = models.ForeignKey('stock.Shift', on_delete=models.SET_NULL, related_name='payouts',
        null=True, blank=True)
    # sale = models.ForeignKey(Sale, related_name='cashouts', null=True, blank=True)

    initiator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='cash_records')

    objects = CashRecordQuerySet.as_manager()

    def __str__(self):
        return self.amount