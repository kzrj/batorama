# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Q, Subquery, OuterRef, Count, Prefetch, F, Sum, Value 
from django.db.models.functions import Coalesce
from django.contrib.auth.models import User
from django.utils import timezone

from core.models import CoreModel, CoreModelManager


class TimberQuerySet(models.QuerySet):
    pass


class Timber(CoreModel):
    SPECIES = [('pine', 'Сосна'), ('larch', 'Лиственница')]
    wood_species = models.CharField(max_length=20, choices=SPECIES)

    diameter = models.IntegerField()
    length = models.IntegerField()
    volume = models.FloatField()

    objects = TimberQuerySet.as_manager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.diameter} {self.wood_species}'


class TimberRecordQuerySet(models.QuerySet):
    # Servises
    def create_for_income_from_list(self, records_list, rama, initiator=None):
        timber_records = list()
        for record in records_list:
            if record['quantity'] > 0:
                timber_records.append(
                    TimberRecord(
                        timber=record['timber'],
                        quantity=record['quantity'],
                        volume=record['quantity']*record['timber'].volume, 
                        rama=rama)
                )
        return self.bulk_create(timber_records)

    # Selectors
    def calc_total_quantity_and_volume(self):
        return self.aggregate(total_qnty=Sum('quantity'), total_volume=Sum('volume'))


class TimberRecord(CoreModel):
    timber = models.ForeignKey(Timber, on_delete=models.CASCADE, related_name='records')

    rama = models.ForeignKey('stock.Rama', on_delete=models.SET_NULL, blank=True, null=True,
     related_name='timber_records')

    quantity = models.IntegerField()
    volume = models.FloatField()

    income_timber = models.ForeignKey('rawstock.IncomeTimber', on_delete=models.SET_NULL, null=True,
     blank=True, related_name='records')

    objects = TimberRecordQuerySet.as_manager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.timber} record'


class IncomeTimberQuerySet(models.QuerySet):
    # Servises
    def create_income_timber(self, raw_timber_records, rama=None, initiator=None, note=None):       
        timber_records = TimberRecord.objects.create_for_income_from_list(
            records_list=raw_timber_records, rama=rama, initiator=initiator)
        timber_records = TimberRecord.objects.filter(pk__in=(tr.pk for tr in timber_records))

        total_qnty_and_volume = timber_records.calc_total_quantity_and_volume()
        income_timber = self.create(initiator=initiator, rama=rama, note=note,
            quantity=total_qnty_and_volume['total_qnty'], volume=total_qnty_and_volume['total_volume'])
        timber_records.update(income_timber=income_timber)

        return income_timber


class IncomeTimber(CoreModel):
    rama = models.ForeignKey('stock.Rama', on_delete=models.SET_NULL, blank=True, null=True,
     related_name='timber_incomes')

    quantity = models.IntegerField()
    volume = models.FloatField()

    initiator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='timber_incomes')

    note = models.CharField(max_length=100, null=True, blank=True)

    objects = IncomeTimberQuerySet.as_manager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.pk} income timber'


class QuotaQuerySet(models.QuerySet):
    # Services
    def create_quota(self, income_timber):
        return self.create(income_timber=income_timber, volume_quota_brus=income_timber.volume*0.5,
            volume_quota_doska=income_timber.volume*0.2, rama=income_timber.rama, 
            initiator=income_timber.initiator)

    # Selectors
    def calc_volume_sum(self):
        return self.aggregate(total_volume_quota_brus=Sum('volume_quota_brus'),
            total_volume_quota_doska=Sum('volume_quota_doska'))


class Quota(CoreModel):
    rama = models.ForeignKey('stock.Rama', on_delete=models.SET_NULL, blank=True, null=True,
     related_name='quotas')

    volume_quota_brus = models.FloatField()
    volume_quota_doska = models.FloatField()

    income_timber = models.OneToOneField(IncomeTimber, on_delete=models.CASCADE)

    initiator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='quotas')

    objects = QuotaQuerySet.as_manager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.diameter} {self.wood_species}'

    def current_quota(self):
        created_volume = self.shifts.calc_created_volume()

        return round(self.volume_quota_brus - created_volume['total_brus_volume'], 3), \
               round(self.volume_quota_doska - created_volume['total_doska_volume'], 3), 
