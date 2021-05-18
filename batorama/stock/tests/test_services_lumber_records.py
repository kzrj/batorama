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

        self.doska4_18 = Lumber.objects.filter(name__contains='доска 4*18')[0]
        self.doska25_18 = Lumber.objects.filter(name__contains='доска 2.5*18')[0]

        self.china_brus1 = Lumber.objects.filter(name='брус 18*18', wood_species='pine',
         china_volume__isnull=False).first()
        self.china_brus2 = Lumber.objects.filter(name='брус 15*18', wood_species='pine',
         china_volume__isnull=False).first()

        self.rama = Rama.objects.all().first()

    def test_create_for_common_sale_exact_calc(self):
        data_list = [
            {'lumber': self.brus1, 'quantity': 10, 'rama_price': 12000, 'selling_price': 12500,
                'selling_total_cash': 7500, 'calc_type': 'exact'},
            {'lumber': self.brus2, 'quantity': 15, 'rama_price': 12000, 'selling_price': 12800,
                'selling_total_cash': 7680, 'calc_type': 'exact'},
            {'lumber': self.doska4_18, 'quantity': 70, 'rama_price': 7000, 'selling_price': 7500,
                'selling_total_cash': 15120, 'calc_type': 'exact'},
            {'lumber': self.doska25_18, 'quantity': 65, 'rama_price': 7000, 'selling_price': 7200,
                'selling_total_cash': 8424, 'calc_type': 'exact'},
        ]

        lumber_records = LumberRecord.objects.create_from_raw_for_common_sale(
            records_list=data_list, rama=self.rama)

        self.assertEqual(LumberRecord.objects.all().count(), 4)

        lr1 = LumberRecord.objects.filter(lumber=self.brus1).first()
        self.assertEqual(lr1.quantity, 10)
        self.assertEqual(lr1.volume, 0.6)
        self.assertEqual(lr1.rama_price, 12000)
        self.assertEqual(lr1.rama_total_cash, lr1.rama_price*lr1.quantity*lr1.lumber.volume)
        self.assertEqual(lr1.selling_price, 12500)
        self.assertEqual(lr1.selling_total_cash, 7500)
        self.assertEqual(lr1.selling_calc_type, 'exact')

    def test_create_for_common_sale_round_calc(self):
        data_list = [
            {'lumber': self.brus1, 'quantity': 10, 'rama_price': 12000, 'selling_price': 12500,
                'selling_total_cash': 7813, 'calc_type': 'round'},
            {'lumber': self.brus2, 'quantity': 15, 'rama_price': 12000, 'selling_price': 12800,
                'selling_total_cash': 7680, 'calc_type': 'round'},
            {'lumber': self.doska4_18, 'quantity': 70, 'rama_price': 7000, 'selling_price': 7500,
                'selling_total_cash': 15443, 'calc_type': 'round'},
            {'lumber': self.doska25_18, 'quantity': 65, 'rama_price': 7000, 'selling_price': 7200,
                'selling_total_cash': 8510, 'calc_type': 'round'},
        ]

        lumber_records = LumberRecord.objects.create_from_raw_for_common_sale(
            records_list=data_list, rama=self.rama)

        self.assertEqual(LumberRecord.objects.all().count(), 4)
        
        lr3 = LumberRecord.objects.filter(lumber=self.doska4_18).first()
        self.assertEqual(lr3.quantity, 70)
        self.assertEqual(lr3.volume, 2.016)
        self.assertEqual(lr3.rama_price, 7000)
        self.assertEqual(lr3.rama_total_cash, lr3.rama_price*lr3.quantity*lr3.lumber.volume)
        self.assertEqual(lr3.selling_price, 7500)
        self.assertEqual(lr3.selling_total_cash, 15443)
        self.assertEqual(lr3.selling_calc_type, 'round')

    def test_create_for_common_sale_china_calc(self):
        data_list = [
            {'lumber': self.china_brus1, 'quantity': 10, 'rama_price': 15000,
             'selling_price': 15000, 'selling_total_cash': 19010, 'calc_type': 'china'},
            {'lumber': self.china_brus2, 'quantity': 15, 'rama_price': 15000,
             'selling_price': 15000, 'selling_total_cash': 23709, 'calc_type': 'china'},
        ]
        lumber_records = LumberRecord.objects.create_from_raw_for_common_sale(
            records_list=data_list, rama=self.rama)

        self.assertEqual(LumberRecord.objects.all().count(), 2)

        lr1 = LumberRecord.objects.filter(lumber=self.china_brus1).first()
        self.assertEqual(lr1.quantity, 10)
        self.assertEqual(lr1.volume, 1.296)
        self.assertEqual(lr1.rama_price, 15000)
        self.assertEqual(lr1.rama_total_cash,
         round(lr1.rama_price*lr1.quantity*lr1.lumber.china_volume, 1))
        self.assertEqual(lr1.selling_price, 15000)
        self.assertEqual(lr1.selling_total_cash, 19010)
        self.assertEqual(lr1.selling_total_cash, round(lr1.rama_total_cash))
        self.assertEqual(lr1.selling_calc_type, 'china')

    def test_create_for_common_sale_mixed_calc(self):
        data_list = [
            {'lumber': self.brus1, 'quantity': 10, 'rama_price': 12000, 'selling_price': 12500,
                'selling_total_cash': 7500, 'calc_type': 'exact'},
            {'lumber': self.china_brus1, 'quantity': 10, 'rama_price': 15000,
                'selling_price': 15000, 'selling_total_cash': 19010, 'calc_type': 'china'},
            {'lumber': self.doska4_18, 'quantity': 70, 'rama_price': 7000, 'selling_price': 7500,
                'selling_total_cash': 15443, 'calc_type': 'round'},
        ]

        lumber_records = LumberRecord.objects.create_from_raw_for_common_sale(
            records_list=data_list, rama=self.rama)

        self.assertEqual(LumberRecord.objects.all().count(), 3)

        lr1 = LumberRecord.objects.filter(lumber=self.brus1).first()
        self.assertEqual(lr1.quantity, 10)
        self.assertEqual(lr1.volume, 0.6)
        self.assertEqual(lr1.rama_price, 12000)
        self.assertEqual(lr1.rama_total_cash, lr1.rama_price*lr1.quantity*lr1.lumber.volume)
        self.assertEqual(lr1.selling_price, 12500)
        self.assertEqual(lr1.selling_total_cash, 7500)
        self.assertEqual(lr1.selling_calc_type, 'exact')

        lr2 = LumberRecord.objects.filter(lumber=self.china_brus1).first()
        self.assertEqual(lr2.quantity, 10)
        self.assertEqual(lr2.volume, 1.296)
        self.assertEqual(lr2.rama_price, 15000)
        self.assertEqual(lr2.rama_total_cash,
         round(lr2.rama_price*lr2.quantity*lr2.lumber.china_volume, 1))
        self.assertEqual(lr2.selling_price, 15000)
        self.assertEqual(lr2.selling_total_cash, 19010)
        self.assertEqual(lr2.selling_total_cash, round(lr2.rama_total_cash))
        self.assertEqual(lr2.selling_calc_type, 'china')
        
        lr3 = LumberRecord.objects.filter(lumber=self.doska4_18).first()
        self.assertEqual(lr3.quantity, 70)
        self.assertEqual(lr3.volume, 2.016)
        self.assertEqual(lr3.rama_price, 7000)
        self.assertEqual(lr3.rama_total_cash, lr3.rama_price*lr3.quantity*lr3.lumber.volume)
        self.assertEqual(lr3.selling_price, 7500)
        self.assertEqual(lr3.selling_total_cash, 15443)
        self.assertEqual(lr3.selling_calc_type, 'round')
        