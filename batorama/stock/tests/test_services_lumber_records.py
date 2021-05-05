# -*- coding: utf-8 -*-
import datetime
from django.test import TestCase, TransactionTestCase
from django.contrib.auth.models import User

from stock.models import Shift, Lumber, LumberRecord, Sale, Rama
from accounts.models import Account

import stock.testing_utils as testing


class LumberRecordsServisesTest(TransactionTestCase):
    def setUp(self):
        testing.create_test_data()

        self.seller1 = User.objects.get(username='seller1')
        self.kladman = User.objects.get(username='kladman')

        self.brus1 = Lumber.objects.filter(name__contains='брус')[0]
        self.brus2 = Lumber.objects.filter(name__contains='брус')[1]
        self.doska1 = Lumber.objects.filter(name__contains='доска')[0]
        self.doska2 = Lumber.objects.filter(name__contains='доска')[1]

        self.rama = Rama.objects.all().first()

    def test_create_sale_schema1(self):
        data_list = [
                {'lumber': self.brus1, 'quantity': 10, 'rama_price': 12000, 'selling_price': 12500,
                    'selling_total_cash': 12510},
                {'lumber': self.brus2, 'quantity': 15, 'rama_price': 12000, 'selling_price': 12800,
                    'selling_total_cash': 7680},
                {'lumber': self.doska1, 'quantity': 70, 'rama_price': 7000, 'selling_price': 7500,
                    'selling_total_cash': 15120},
                {'lumber': self.doska2, 'quantity': 55, 'rama_price': 7000, 'selling_price': 7200,
                    'selling_total_cash': 9504},
            ]
            
        lumber_records = LumberRecord.objects.create_from_list_sale_schema1(
            records_list=data_list, rama=self.rama)

        self.assertEqual(LumberRecord.objects.all().count(), 4)

        lr1 = LumberRecord.objects.filter(lumber=self.brus1).first()
        self.assertEqual(lr1.quantity, 10)
        self.assertEqual(lr1.volume, 0.6)
        self.assertEqual(lr1.rama_price, 12000)
        self.assertEqual(lr1.rama_total_cash, lr1.rama_price*lr1.quantity*lr1.lumber.volume)
        self.assertEqual(lr1.selling_price, 12500)
        self.assertEqual(lr1.selling_total_cash, 12510)
