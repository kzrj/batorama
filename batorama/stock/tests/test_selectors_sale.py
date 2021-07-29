# -*- coding: utf-8 -*-
import datetime
from django.test import TestCase, TransactionTestCase
from django.contrib.auth.models import User

from stock.models import Shift, Lumber, LumberRecord, Sale, Rama
from accounts.models import Account

import stock.testing_utils as testing


class SaleServisesTest(TransactionTestCase):
    def setUp(self):
        testing.create_init_data()

        self.seller1 = User.objects.get(username='seller1')
        self.kladman = User.objects.get(username='kladman')

        self.brus1 = Lumber.objects.filter(name__contains='брус', wood_species='pine')[0]
        self.brus2 = Lumber.objects.filter(name__contains='брус', wood_species='pine')[1]
        self.doska1 = Lumber.objects.filter(name__contains='доска', wood_species='pine')[0]
        self.doska2 = Lumber.objects.filter(name__contains='доска', wood_species='pine')[1]

        self.china_brus1 = Lumber.objects.filter(name='брус 18*18', wood_species='pine',
         china_volume__isnull=False).first()
        self.china_brus2 = Lumber.objects.filter(name='брус 15*18', wood_species='pine',
         china_volume__isnull=False).first()

        self.doska4_18 = Lumber.objects.filter(name__contains='доска 4*18', wood_species='pine')[0]
        self.doska25_18 = Lumber.objects.filter(name__contains='доска 2.5*18', wood_species='pine')[0]

        self.rama = Rama.objects.all().first()

        data_list = {
            'lumbers': [
                {'lumber': self.brus1, 'quantity': 10, 'rama_price': 12000, 'selling_price': 12500,
                    'selling_total_cash': 7500, 'calc_type': 'exact'},
                {'lumber': self.china_brus1, 'quantity': 10, 'rama_price': 15000,
                    'selling_price': 15000, 'selling_total_cash': 19010, 'calc_type': 'china'},
                {'lumber': self.doska4_18, 'quantity': 70, 'rama_price': 7000, 'selling_price': 7500,
                    'selling_total_cash': 15443, 'calc_type': 'round'},
            ],
            'loader': True,
            'seller': self.seller1,
            'bonus_kladman': self.kladman,
            'delivery_fee': 500,
            'add_expenses': 0,
            'note': '',
            'client': 'Баярма'
        }

        self.sale1 = Sale.objects.create_sale_common(
            raw_records=data_list['lumbers'],
            initiator=self.kladman,
            loader=data_list['loader'],
            delivery_fee=data_list['delivery_fee'],
            add_expenses=data_list['add_expenses'],
            note=data_list['note'],
            client=data_list['client'],
            seller=data_list['seller'],
            bonus_kladman=data_list['bonus_kladman']
            )

        data_list2 = {
            'lumbers': [
                {'lumber': self.brus1, 'quantity': 13, 'rama_price': 12000, 'selling_price': 12500,
                    'selling_total_cash': 7500, 'calc_type': 'exact'},
                {'lumber': self.china_brus1, 'quantity': 5, 'rama_price': 15000,
                    'selling_price': 15000, 'selling_total_cash': 19010, 'calc_type': 'china'},
                {'lumber': self.doska25_18, 'quantity': 53, 'rama_price': 7000, 'selling_price': 7500,
                    'selling_total_cash': 15443, 'calc_type': 'round'},
            ],
            'loader': True,
            'seller': self.seller1,
            'bonus_kladman': self.kladman,
            'delivery_fee': 500,
            'add_expenses': 0,
            'note': '',
            'client': 'Баярма'
        }

        self.sale2 = Sale.objects.create_sale_common(
            raw_records=data_list2['lumbers'],
            initiator=self.kladman,
            loader=data_list2['loader'],
            delivery_fee=data_list2['delivery_fee'],
            add_expenses=data_list2['add_expenses'],
            note=data_list2['note'],
            client=data_list2['client'],
            seller=data_list2['seller'],
            bonus_kladman=data_list2['bonus_kladman']
            )

    def test_calc_sold_volume_for_quota_calc(self):
        s1 = Sale.objects.all().add_only_brus_volume().add_only_doska_volume_exclude_2_5() \
            .get(pk=self.sale1.pk)
        s2 = Sale.objects.all().add_only_brus_volume().add_only_doska_volume_exclude_2_5() \
            .get(pk=self.sale2.pk)

        self.assertEqual(s1.brus_volume, 1.896)
        self.assertEqual(s1.doska_volume, 2.016)

        self.assertEqual(s2.brus_volume, 1.428)
        self.assertEqual(s2.doska_volume, 0.0)

        total_sold_volume = Sale.objects.all().calc_sold_volume_for_quota_calc()
        self.assertEqual(total_sold_volume['total_brus_volume'], 1.896 + 1.428)
        self.assertEqual(total_sold_volume['total_doska_volume'], 2.016)