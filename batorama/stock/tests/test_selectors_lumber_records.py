# -*- coding: utf-8 -*-
import datetime
from django.test import TestCase, TransactionTestCase
from django.contrib.auth.models import User

from stock.models import Shift, Lumber, LumberRecord, Sale, Rama
from accounts.models import Account

import stock.testing_utils as testing


class LumberRecordsSelectorsTest(TransactionTestCase):
    def setUp(self):
        testing.create_test_data()

        self.seller1 = User.objects.get(username='seller1')
        self.kladman = User.objects.get(username='kladman')

        self.brus1 = Lumber.objects.filter(name__contains='брус')[0]
        self.brus2 = Lumber.objects.filter(name__contains='брус')[1]
        self.doska1 = Lumber.objects.filter(name__contains='доска')[0]
        self.doska2 = Lumber.objects.filter(name__contains='доска')[1]

        self.rama = Rama.objects.all().first()

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
            
        lumber_records = LumberRecord.objects.create_from_raw_for_common_sale(
            records_list=data_list, rama=self.rama)

        self.lumber_records_qs = LumberRecord.objects.filter(pk__in=(lr.pk for lr in lumber_records))

    def test_calc_rama_total_cash(self):
        self.assertEqual(self.lumber_records_qs.calc_rama_total_cash(), 7200 + 7200 + 14112 + 9240)

    def test_calc_selling_total_cash(self):
        self.assertEqual(self.lumber_records_qs.calc_selling_total_cash(), 44814)

    def test_calc_sale_volume_and_cash_schema1(self):
        data_for_sale_schema1 = self.lumber_records_qs.calc_sale_volume_and_cash()
        self.assertEqual(data_for_sale_schema1['total_volume'], round(0.6 + 0.6 + 2.016 + 1.32, 4))
        self.assertEqual(data_for_sale_schema1['rama_cash'], 7200 + 7200 + 14112 + 9240)
        self.assertEqual(data_for_sale_schema1['sale_cash'], 44814)
