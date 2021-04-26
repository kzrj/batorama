# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Q, Subquery, OuterRef, Count, Prefetch, F, Sum
from django.contrib.auth.models import User
from django.utils import timezone

from core.models import CoreModel, CoreModelManager


class RoundLumberIncome(CoreModel):
    date = models.DateTimeField(null=True, blank=True)
    rama = models.ForeignKey('stock.Rama', on_delete=models.SET_NULL, null=True, blank=True)
    volume = models.FloatField()
    cost = models.IntegerField()
    work_cost = models.IntegerField()

    cost_payed = models.BooleanField(default=False)
    work_cost_payed = models.BooleanField(default=False)

    sawned = models.BooleanField(default=False)

    def __str__(self):
        return f'round income {self.volume}m3'
    

class Quota(CoreModel):
    rama = models.OneToOneField('stock.Rama', on_delete=models.SET_NULL, null=True, blank=True)