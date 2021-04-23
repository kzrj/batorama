# # -*- coding: utf-8 -*-
from django.contrib.auth.models import User

from stock.models import (Lumber, Shift, LumberRecord, Rama)
from accounts.models import (Account, CashRecord)


def get_stock(rama_title):
    rama = Rama.objects.get(name=rama_title)
    Shift.objects.filter(rama=rama)
    