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
     blank=True, related_name='timber_records')

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

        Quota.objects.create_quota(income_timber=income_timber)

        income_timber.cash_records.create_income_timber_payment_to_manager(
            income_timber=income_timber,
            amount=income_timber.volume*0.75*1100,
            initiator=initiator,
            manager=initiator.account,
            note=None
            )

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
        data = dict()

        pine_volume = income_timber.timber_records.filter(timber__wood_species='pine') \
            .aggregate(volume=Sum('volume'))['volume']
        larch_volume = income_timber.timber_records.filter(timber__wood_species='larch') \
            .aggregate(volume=Sum('volume'))['volume']

        if pine_volume and pine_volume > 0:
            data['pine_quota'] = self.create(income_timber=income_timber, rama=income_timber.rama, 
                volume_quota_brus=pine_volume*0.5,
                volume_quota_doska=pine_volume*0.25,
                initiator=income_timber.initiator, wood_species='pine')
        else:
            data['pine_quota'] = None

        if larch_volume and larch_volume > 0:
            data['larch_quota'] = self.create(income_timber=income_timber, rama=income_timber.rama, 
                volume_quota_brus=larch_volume*0.5,
                volume_quota_doska=larch_volume*0.25,
                initiator=income_timber.initiator, wood_species='larch')
        else:
            data['larch_quota'] = None

        return data

    # Selectors
    def calc_volume_sum(self):
        return self.aggregate(total_volume_quota_brus=Coalesce(Sum('volume_quota_brus'), 0.0),
            total_volume_quota_doska=Coalesce(Sum('volume_quota_doska'), 0.0))

    def curent_rama_quota(self, rama, wood_species):
        quotas_volumes = self.filter(rama=rama, wood_species=wood_species).calc_volume_sum()
        sold_volumes = rama.sales.calc_sold_volume_for_quota_calc(wood_species=wood_species)

        data = dict()
        data['total_volume_quota_brus'] = quotas_volumes['total_volume_quota_brus']
        data['total_volume_quota_doska'] = quotas_volumes['total_volume_quota_doska']
        data['total_volume_sold_brus'] = sold_volumes['total_brus_volume']
        data['total_volume_sold_doska'] = sold_volumes['total_doska_volume']
        data['brus_balance'] = quotas_volumes['total_volume_quota_brus'] - \
            sold_volumes['total_brus_volume']
        data['doska_balance'] = quotas_volumes['total_volume_quota_doska'] - \
            sold_volumes['total_doska_volume']

        return data


class Quota(CoreModel):
    SPECIES = [('pine', 'Сосна'), ('larch', 'Лиственница')]
    wood_species = models.CharField(max_length=20, choices=SPECIES)

    rama = models.ForeignKey('stock.Rama', on_delete=models.SET_NULL, blank=True, null=True,
     related_name='quotas')

    volume_quota_brus = models.FloatField()
    volume_quota_doska = models.FloatField()

    income_timber = models.ForeignKey(IncomeTimber, on_delete=models.CASCADE, related_name='quotas',
        blank=True, null=True,)

    initiator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='quotas')

    objects = QuotaQuerySet.as_manager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'План {self.pk}'

    def current_quota(self):
        sold_volume = self.rama.sales.calc_sold_volume_for_quota_calc()
        
        return round(self.volume_quota_brus - sold_volume['total_brus_volume'], 3), \
               round(self.volume_quota_doska - sold_volume['total_doska_volume'], 3), 

