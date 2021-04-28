# # -*- coding: utf-8 -*-
from django.contrib.auth.models import User

from stock.models import (Lumber, Shift, LumberRecord, Rama)
from accounts.models import (Account, CashRecord)


def get_stock(rama_title):
    rama = Rama.objects.get(name=rama_title)
    
    Lumber.objects.all().annotate(
    	records__shift__is_null=False,

    	)
    

def calc_total_income_volume_by_rama_by_lumber(lumber, rama):
	return LumberRecord.objects.filter(lumber=lumber, rama=rama, shift__isnull=False) \
            .values('rama') \
            .annotate(total_income_volume=Sum('volume')) \
            .values('total_income_volume')

def calc_total_income_volume_by_rama_by_lumber(lumber, rama):
	return LumberRecord.objects.filter(lumber=lumber, rama=rama, shift__isnull=False) \
            .values('rama') \
            .annotate(total_income_volume=Sum('volume')) \
            .values('total_income_volume')
