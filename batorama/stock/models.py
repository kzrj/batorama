# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Q, Subquery, OuterRef, Count, Prefetch, F, Sum
from django.contrib.auth.models import User
from django.utils import timezone

from core.models import CoreModel, CoreModelManager


class EmployeeQuerySet(models.QuerySet):
    pass


class Employee(CoreModel):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="employee")

    is_ramshik = models.BooleanField(default=False)
    is_senior_ramshik = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)

    objects = EmployeeQuerySet.as_manager()

    def __str__(self):
        return self.user.username


class LumberQuerySet(models.QuerySet):
    pass


class Lumber(CoreModel):
    name = models.CharField(max_length=100)
    width = models.FloatField()
    length = models.FloatField()
    height = models.FloatField()
    volume = models.FloatField()
    employee_rate = models.IntegerField(default=0)

    objects = LumberQuerySet.as_manager()

    def __str__(self):
        return self.name


class ShiftQuerySet(models.QuerySet):
    def create_shift(self, shift_type, employees, lumber_records, initiator=None, date=None):
        if not date:
            date = timezone.now()
        shift = self.create(shift_type=shift_type, date=date)
        shift.employees.add(*employees)
        lumber_records.update(shift=shift)
        shift.initiator = initiator
        shift.volume = lumber_records.calc_total_volume()
        shift.employee_cash = lumber_records.calc_total_cash()
        shift.cash_per_employee = shift.employee_cash / len(employees)
        shift.save()

        return shift

    def create_shift_raw_records(self, **kwargs):
        lumber_records = LumberRecord.objects.create_from_list(records_list=kwargs['raw_records'])
        kwargs['lumber_records'] = LumberRecord.objects.filter(pk__in=(lr.pk for lr in lumber_records))
        del kwargs['raw_records']
        return self.create_shift(**kwargs)


class Shift(CoreModel):
    date = models.DateTimeField(null=True, blank=True)
    SHIFT_TYPES = [('day', 'День'), ('night', 'Ночь')]

    shift_type = models.CharField(max_length=10, choices=SHIFT_TYPES)

    employees = models.ManyToManyField(Employee)
    initiator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='shifts')

    volume = models.FloatField(null=True)

    employee_cash = models.FloatField(null=True)
    cash_per_employee = models.FloatField(null=True)

    objects = ShiftQuerySet.as_manager()

    class Meta:
        ordering = ['date',]

    def __str__(self):
        return f'Cмена {self.shift_type} {self.date.strftime("%d-%m-%Y")}'


class LumberRecordQuerySet(models.QuerySet):
    def create_from_list(self, records_list):
        lumber_records = list()
        for record in records_list:
            lumber_records.append(LumberRecord(lumber=record['lumber'], quantity=record['quantity'],
                volume=record['volume'], employee_rate=record['employee_rate'],
                employee_total_cash=record['total']))
        return self.bulk_create(lumber_records)

    def calc_total_volume(self):
        return self.aggregate(total_volume=Sum('volume'))['total_volume']

    def calc_total_cash(self):
        return self.aggregate(total_cash=Sum('employee_total_cash'))['total_cash']


class LumberRecord(CoreModel):
    lumber = models.ForeignKey(Lumber, on_delete=models.CASCADE, related_name='records')
    quantity = models.IntegerField(default=0)
    volume = models.FloatField(default=0)
    employee_rate = models.IntegerField(default=0)
    employee_total_cash = models.FloatField(default=0)

    shift = models.ForeignKey(Shift, on_delete=models.CASCADE, null=True, related_name='lumber_records')

    # sale = models.ForeignKey(Sale, related_name='lumbers_records')
    # price = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)

    objects = LumberRecordQuerySet.as_manager()

    def __str__(self):
        return f'{self.lumber} {self.quantity}'


class CashRecordQuerySet(models.QuerySet):
    pass


class CashRecord(CoreModel):
    amount = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='payouts',
     null=True, blank=True)

    # sale = models.ForeignKey(Sale, related_name='cashouts', null=True, blank=True)

    objects = CashRecordQuerySet.as_manager()

    def __str__(self):
        return self.amount