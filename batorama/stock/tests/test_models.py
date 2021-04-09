# -*- coding: utf-8 -*-
import datetime
from django.test import TestCase, TransactionTestCase
from django.contrib.auth.models import User

from stock.models import Shift, Lumber, LumberRecord

import stock.testing_utils as testing


class OsnTest(TransactionTestCase):
    def setUp(self):
        testing.create_test_data()

        self.ramshik1 = User.objects.get(username='ramshik1')
        self.ramshik2 = User.objects.get(username='ramshik2')
        self.ramshik3 = User.objects.get(username='ramshik3')
        self.ramshik4 = User.objects.get(username='ramshik4')

        self.brus1 = Lumber.objects.filter(name__contains='брус')[0]
        self.brus2 = Lumber.objects.filter(name__contains='брус')[1]
        self.doska1 = Lumber.objects.filter(name__contains='доска')[0]
        self.doska2 = Lumber.objects.filter(name__contains='доска')[1]

    def test_create_from_shift_list(self):
        data_list = [
            {'lumber': self.brus1, 'quantity': 10, 'volume': 0.6, 'employee_rate': 600, 'total': 360 },
            {'lumber': self.brus2, 'quantity': 10, 'volume': 0.4, 'employee_rate': 600, 'total': 240 },
            {'lumber': self.doska1, 'quantity': 50, 'volume': 1.44, 'employee_rate': 600, 'total': 864 },
            {'lumber': self.doska2, 'quantity': 40, 'volume': 0.96, 'employee_rate': 600, 'total': 576 },
        ]

        lrs = LumberRecord.objects.create_from_list(records_list=data_list)
        self.assertEqual(LumberRecord.objects.all().count(), 4)

    def test_create_shift(self):
        employees = [self.ramshik1.employee, self.ramshik2.employee, self.ramshik3.employee]
        data_list = [
            {'lumber': self.brus1, 'quantity': 10, 'volume': 0.6, 'employee_rate': 600, 'total': 360 },
            {'lumber': self.brus2, 'quantity': 10, 'volume': 0.4, 'employee_rate': 600, 'total': 240 },
            {'lumber': self.doska1, 'quantity': 50, 'volume': 1.44, 'employee_rate': 600, 'total': 864 },
            {'lumber': self.doska2, 'quantity': 40, 'volume': 0.96, 'employee_rate': 600, 'total': 576 },
        ]
        LumberRecord.objects.create_from_list(records_list=data_list)
        lumber_records = LumberRecord.objects.all()

        shift = Shift.objects.create_shift(shift_type='day', employees=employees, 
            lumber_records=lumber_records)

        self.assertEqual(shift.volume, 3.4)
        self.assertEqual(shift.employee_cash, 2040)
        self.assertEqual(shift.cash_per_employee, 680)

    def test_create_shift_raw_records(self):
        employees = [self.ramshik1.employee, self.ramshik2.employee, self.ramshik3.employee]
        data_list = [
            {'lumber': self.brus1, 'quantity': 10, 'volume': 0.6, 'employee_rate': 600, 'total': 360 },
            {'lumber': self.brus2, 'quantity': 10, 'volume': 0.4, 'employee_rate': 600, 'total': 240 },
            {'lumber': self.doska1, 'quantity': 50, 'volume': 1.44, 'employee_rate': 600, 'total': 864 },
            {'lumber': self.doska2, 'quantity': 40, 'volume': 0.96, 'employee_rate': 600, 'total': 576 },
        ]

        shift = Shift.objects.create_shift_raw_records(shift_type='day', employees=employees, 
            raw_records=data_list)

        self.assertEqual(shift.volume, 3.4)
        self.assertEqual(shift.employee_cash, 2040)
        self.assertEqual(shift.cash_per_employee, 680)

