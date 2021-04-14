# -*- coding: utf-8 -*-
import datetime
from django.test import TestCase, TransactionTestCase
from django.contrib.auth.models import User

from stock.models import Shift, Lumber, LumberRecord
from accounts.models import Account, CashRecord

import stock.testing_utils as testing


class OsnAccountTest(TransactionTestCase):
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

    def test_create_shift_raw_records(self):
        employees = [self.ramshik1.account, self.ramshik2.account, self.ramshik3.account]
        data_list = [
            {'lumber': self.brus1, 'quantity': 10, 'volume_total': 0.6, 'employee_rate': 600, 'cash': 360 },
            {'lumber': self.brus2, 'quantity': 10, 'volume_total': 0.4, 'employee_rate': 600, 'cash': 240 },
            {'lumber': self.doska1, 'quantity': 50, 'volume_total': 1.44, 'employee_rate': 600, 'cash': 864 },
            {'lumber': self.doska2, 'quantity': 40, 'volume_total': 0.96, 'employee_rate': 600, 'cash': 576 },
        ]

        shift = Shift.objects.create_shift_raw_records(shift_type='day', employees=employees, 
            raw_records=data_list)

        self.assertEqual(shift.volume, 3.4)
        self.assertEqual(shift.employee_cash, 2040)
        self.assertEqual(shift.cash_per_employee, 680)

        self.assertEqual(self.ramshik1.account.cash, 680)
        self.assertEqual(self.ramshik2.account.cash, 680)
        self.assertEqual(self.ramshik3.account.cash, 680)

        self.assertEqual(CashRecord.objects.all().count(), 3)
        for cr in CashRecord.objects.all():
            self.assertEqual(cr.shift, shift)
            self.assertEqual(cr.amount, shift.cash_per_employee)

    def test_create_withdraw_employee(self):
        employee = self.ramshik1.account
        CashRecord.objects.create_withdraw_employee(employee=employee, amount=1000, 
            initiator=self.ramshik1)

        self.assertEqual(employee.cash, -1000)
        self.assertEqual(CashRecord.objects.all().count(), 1)
        self.assertEqual(CashRecord.objects.all().first().record_type, 'withdraw_employee')
        self.assertEqual(CashRecord.objects.all().first().initiator, self.ramshik1)
