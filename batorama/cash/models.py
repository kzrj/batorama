# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Q, Subquery, OuterRef, Count, Prefetch, F, Sum, Value 
from django.db.models.functions import Coalesce
from django.contrib.auth.models import User
from django.utils import timezone

from core.models import CoreModel, CoreModelManager


class CashRecordQuerySet(models.QuerySet):
    # Servises
    def create_payout_from_shift(self, employee, shift, amount, note=None, initiator=None,
         rama=None):
        self.create(amount=amount, account=employee, shift=shift, record_type='payout_to_employee_from_shift',
            initiator=initiator, rama=rama, note=note)
        employee.add_cash(amount)

    def create_withdraw_employee(self, employee, amount, initiator=None, rama=None, note=None):
        self.create(amount=amount, account=employee, record_type='withdraw_employee', 
            initiator=initiator, rama=rama, note=note)
        employee.remove_cash(amount)

    def create_withdraw_cash_from_manager(self, manager_account, amount, initiator=None,
         rama=None):
        return self.create(amount=amount, account=manager_account, 
            record_type='withdraw_cash_from_manager', initiator=initiator, rama=rama)

    def create_rama_expense(self, amount, note, initiator, rama):
        return self.create(amount=amount, note=note, rama=rama, initiator=initiator,
            record_type='rama_expenses')

    def create_income_from_sale(self, amount, note, initiator, rama, sale):
        return self.create(amount=amount, note=note, rama=rama, initiator=initiator,
            sale=sale, record_type='sale_income')

    # Selectors
    def calc_sum(self):
        return self.aggregate(total=Sum('amount'))['total']

    def calc_sum_incomes_expenses(self):
        return self.aggregate(total=
            Coalesce(Sum('amount', filter=Q(record_type='sale_income')), Value(0))
            - Coalesce(Sum('amount', filter=Q(record_type='rama_expenses')), Value(0))
            - Coalesce(Sum('amount', filter=Q(record_type='withdraw_employee')), Value(0))
        )['total']


class CashRecord(CoreModel):
    amount = models.IntegerField()
    RECORD_TYPES = [
        ('payout_to_employee_from_shift', 'Начисление работникам'),
        ('withdraw_employee', 'Обналичивание работникам'),
        ('withdraw_cash_from_manager', 'Вывод средств от кладмэна/менеджера'),
        ('rama_expenses', 'Расходы рамы'),
        ('sale_income', 'Приход с продажи'),
    ]
    record_type = models.CharField(max_length=50, choices=RECORD_TYPES)

    rama = models.ForeignKey('stock.Rama', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='cash_records')

    account = models.ForeignKey('accounts.Account', on_delete=models.SET_NULL, 
        related_name='cash_records', null=True, blank=True)

    shift = models.ForeignKey('stock.Shift', on_delete=models.SET_NULL, related_name='payouts',
        null=True, blank=True)
    sale = models.ForeignKey('stock.Sale', on_delete=models.SET_NULL, related_name='cash_records',
        null=True, blank=True)

    initiator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='cash_records')

    note = models.CharField(max_length=200, null=True, blank=True)

    objects = CashRecordQuerySet.as_manager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str(self.amount)