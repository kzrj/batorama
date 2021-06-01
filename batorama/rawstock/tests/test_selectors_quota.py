# -*- coding: utf-8 -*-
import datetime
from django.test import TestCase, TransactionTestCase
from django.contrib.auth.models import User

from stock.models import Rama, Shift, Lumber
from rawstock.models import Timber, TimberRecord, IncomeTimber, Quota

import stock.testing_utils as lumber_testing
import rawstock.testing_utils as timber_testing


class LumberRecordsServisesTest(TransactionTestCase):
    def setUp(self):
        lumber_testing.create_test_data()
        timber_testing.create_test_timber()

        self.seller1 = User.objects.get(username='seller1')
        self.kladman = User.objects.get(username='kladman')

        self.ramshik1 = User.objects.get(username='ramshik1')
        self.ramshik2 = User.objects.get(username='ramshik2')
        self.ramshik3 = User.objects.get(username='ramshik3')
        self.ramshik4 = User.objects.get(username='ramshik4')

        self.pine_timber20 = Timber.objects.get(diameter=20, wood_species='pine')
        self.pine_timber22 = Timber.objects.get(diameter=22, wood_species='pine')
        self.pine_timber28 = Timber.objects.get(diameter=28, wood_species='pine')

        self.brus1 = Lumber.objects.filter(name__contains='брус')[0]
        self.brus2 = Lumber.objects.filter(name__contains='брус')[1]
        self.doska1 = Lumber.objects.filter(name__contains='доска')[0]
        self.doska2 = Lumber.objects.filter(name__contains='доска')[1]

        self.rama = Rama.objects.all().first()

        data_list = [
            {'timber': self.pine_timber20, 'quantity': 20 },
            {'timber': self.pine_timber22, 'quantity': 25 },
            {'timber': self.pine_timber28, 'quantity': 30 },
        ]

        self.income_timber = IncomeTimber.objects.create_income_timber(raw_timber_records=data_list,
            initiator=self.kladman)

    def test_current_quota(self):
        quota = Quota.objects.create_quota(income_timber=self.income_timber)
        employees = [self.ramshik1.account, self.ramshik2.account, self.ramshik3.account]
        data_list = [
            {'lumber': self.brus1, 'quantity': 10, 'volume_total': 0.6, 'rate': 600, 'cash': 360 },
            {'lumber': self.brus2, 'quantity': 10, 'volume_total': 0.4, 'rate': 600, 'cash': 240 },
            {'lumber': self.doska1, 'quantity': 50, 'volume_total': 1.44, 'rate': 600, 'cash': 864 },
            {'lumber': self.doska2, 'quantity': 40, 'volume_total': 0.96, 'rate': 600, 'cash': 576 },
        ]

        shift = Shift.objects.create_shift_with_quota_calc(shift_type='day', 
            employees=employees, raw_records=data_list, cash=1200, 
            initiator=self.ramshik1, rama=self.rama, quota=quota)

        self.assertEqual(shift.quota, quota)
        shifts = Shift.objects.all().add_only_brus_volume().add_only_doska_volume()

        self.assertEqual(shifts.first().brus_volume, 1.0)
        self.assertEqual(shifts.first().doska_volume, 2.4)

        quota.refresh_from_db()
        self.assertEqual(quota.current_quota(), (7.045, 0.818))