# -*- coding: utf-8 -*-
import datetime
from django.test import TestCase, TransactionTestCase
from django.contrib.auth.models import User

from stock.models import Shift, Lumber, LumberRecord, Sale, Rama
from rawstock.models import Quota, IncomeTimber, Timber
from accounts.models import Account

import stock.testing_utils as lumber_testing
import rawstock.testing_utils as timber_testing


class ShiftServicesTest(TransactionTestCase):
    def setUp(self):
        lumber_testing.create_test_data()

        self.ramshik1 = User.objects.get(username='ramshik1')
        self.ramshik2 = User.objects.get(username='ramshik2')
        self.ramshik3 = User.objects.get(username='ramshik3')
        self.ramshik4 = User.objects.get(username='ramshik4')

        self.brus1 = Lumber.objects.filter(name__contains='брус')[0]
        self.brus2 = Lumber.objects.filter(name__contains='брус')[1]
        self.doska1 = Lumber.objects.filter(name__contains='доска')[0]
        self.doska2 = Lumber.objects.filter(name__contains='доска')[1]

        self.rama = Rama.objects.all().first()

    def test_create_from_shift_list(self):
        data_list = [
            {'lumber': self.brus1, 'quantity': 10, 'volume_total': 0.6, 'rate': 600, 'cash': 360 },
            {'lumber': self.brus2, 'quantity': 10, 'volume_total': 0.4, 'rate': 600, 'cash': 240 },
            {'lumber': self.doska1, 'quantity': 50, 'volume_total': 1.44, 'rate': 600, 'cash': 864 },
            {'lumber': self.doska2, 'quantity': 40, 'volume_total': 0.96, 'rate': 600, 'cash': 576 },
        ]

        lrs = LumberRecord.objects.create_from_list(records_list=data_list)
        self.assertEqual(LumberRecord.objects.all().count(), 4)

    def test_create_shift(self):
        employees = [self.ramshik1.account, self.ramshik2.account, self.ramshik3.account]
        data_list = [
            {'lumber': self.brus1, 'quantity': 10, 'volume_total': 0.6, 'rate': 600, 'cash': 360 },
            {'lumber': self.brus2, 'quantity': 10, 'volume_total': 0.4, 'rate': 600, 'cash': 240 },
            {'lumber': self.doska1, 'quantity': 50, 'volume_total': 1.44, 'rate': 600, 'cash': 864 },
            {'lumber': self.doska2, 'quantity': 40, 'volume_total': 0.96, 'rate': 600, 'cash': 576 },
        ]
        LumberRecord.objects.create_from_list(records_list=data_list)
        lumber_records = LumberRecord.objects.all()

        shift = Shift.objects.create_shift(shift_type='day', employees=employees, 
            lumber_records=lumber_records, cash=1200, initiator=self.ramshik1)

        self.assertEqual(shift.back_calc_volume, 3.4)
        self.assertEqual(shift.back_calc_cash, 2040)
        self.assertEqual(shift.back_calc_cash_per_employee, 680)
        self.assertEqual(shift.cash_per_employee, 400)
        self.assertEqual(shift.employee_cash, 1200)
        # self.assertEqual(shift.volume, 10)
        self.assertEqual(shift.rama, self.rama)

    def test_create_shift_raw_records(self):
        employees = [self.ramshik1.account, self.ramshik2.account, self.ramshik3.account]
        data_list = [
            {'lumber': self.brus1, 'quantity': 10, 'volume_total': 0.6, 'rate': 600, 'cash': 360 },
            {'lumber': self.brus2, 'quantity': 10, 'volume_total': 0.4, 'rate': 600, 'cash': 240 },
            {'lumber': self.doska1, 'quantity': 50, 'volume_total': 1.44, 'rate': 600, 'cash': 864 },
            {'lumber': self.doska2, 'quantity': 40, 'volume_total': 0.96, 'rate': 600, 'cash': 576 },
        ]

        shift = Shift.objects.create_shift_raw_records(shift_type='day', employees=employees, 
            raw_records=data_list, cash=1200, initiator=self.ramshik1, rama=self.rama)

        self.assertEqual(shift.back_calc_volume, 3.4)
        self.assertEqual(shift.back_calc_cash, 2040)
        self.assertEqual(shift.back_calc_cash_per_employee, 680)
        self.assertEqual(shift.cash_per_employee, 400)
        self.assertEqual(shift.employee_cash, 1200)
        # self.assertEqual(shift.volume, 10)
        self.assertEqual(shift.rama, self.rama)


class ShiftServicesWithQuotaTest(TransactionTestCase):
    def setUp(self):
        lumber_testing.create_test_data()
        timber_testing.create_test_timber()

        self.ramshik1 = User.objects.get(username='ramshik1')
        self.ramshik2 = User.objects.get(username='ramshik2')
        self.ramshik3 = User.objects.get(username='ramshik3')
        self.ramshik4 = User.objects.get(username='ramshik4')
        self.kladman = User.objects.get(username='kladman')

        self.brus1 = Lumber.objects.filter(name__contains='брус')[0]
        self.brus2 = Lumber.objects.filter(name__contains='брус')[1]
        self.doska1 = Lumber.objects.filter(name__contains='доска')[0]
        self.doska2 = Lumber.objects.filter(name__contains='доска')[1]

        self.rama = Rama.objects.all().first()

        self.pine_timber20 = Timber.objects.get(diameter=20, wood_species='pine')
        self.pine_timber22 = Timber.objects.get(diameter=22, wood_species='pine')
        self.pine_timber28 = Timber.objects.get(diameter=28, wood_species='pine')

        data_list = [
            {'timber': self.pine_timber20, 'quantity': 20 },
            {'timber': self.pine_timber22, 'quantity': 25 },
            {'timber': self.pine_timber28, 'quantity': 30 },
        ]

        self.income_timber = IncomeTimber.objects.create_income_timber(raw_timber_records=data_list,
            initiator=self.kladman)

        self.quota = Quota.objects.create_quota(income_timber=self.income_timber)

    def test_create_shift_with_quota_calc(self):
        employees = [self.ramshik1.account, self.ramshik2.account, self.ramshik3.account]
        data_list = [
            {'lumber': self.brus1, 'quantity': 10, 'volume_total': 0.6, 'rate': 600, 'cash': 360 },
            {'lumber': self.brus2, 'quantity': 10, 'volume_total': 0.4, 'rate': 600, 'cash': 240 },
            {'lumber': self.doska1, 'quantity': 50, 'volume_total': 1.44, 'rate': 600, 'cash': 864 },
            {'lumber': self.doska2, 'quantity': 40, 'volume_total': 0.96, 'rate': 600, 'cash': 576 },
        ]

        shift = Shift.objects.create_shift_with_quota_calc(shift_type='day', 
            employees=employees, raw_records=data_list, cash=1200, 
            initiator=self.ramshik1, rama=self.rama, quota=self.quota)

        self.assertEqual(shift.quota, self.quota)
        shifts = Shift.objects.all().add_only_brus_volume().add_only_doska_volume()

        self.assertEqual(shifts.first().brus_volume, 1.0)
        self.assertEqual(shifts.first().doska_volume, 2.4)

        self.quota.refresh_from_db()
        # print('self.quota.volume_quota_brus', self.quota.volume_quota_brus)
        # print(shifts.first().brus_volume)
        # print('self.quota.volume_quota_doska', self.quota.volume_quota_doska)
        # print(shifts.first().doska_volume)
        self.assertEqual(self.quota.current_quota(), (7.045, 0.818))
