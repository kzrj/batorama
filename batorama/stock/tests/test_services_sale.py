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

        self.brus1 = Lumber.objects.filter(name__contains='брус')[0]
        self.brus2 = Lumber.objects.filter(name__contains='брус')[1]
        self.doska1 = Lumber.objects.filter(name__contains='доска')[0]
        self.doska2 = Lumber.objects.filter(name__contains='доска')[1]

        self.china_brus1 = Lumber.objects.filter(name='брус 18*18', wood_species='pine',
         china_volume__isnull=False).first()
        self.china_brus2 = Lumber.objects.filter(name='брус 15*18', wood_species='pine',
         china_volume__isnull=False).first()

        self.doska4_18 = Lumber.objects.filter(name__contains='доска 4*18')[0]
        self.doska25_18 = Lumber.objects.filter(name__contains='доска 2.5*18')[0]

        self.rama = Rama.objects.all().first()

    def test_create_common_sale(self):
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

        sale = Sale.objects.create_sale_common(
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

        self.assertEqual(sale.volume, round(0.6 + 1.296 + 2.016, 4))
        self.assertEqual(sale.seller, self.seller1)
        self.assertEqual(sale.bonus_kladman, self.kladman)
        self.assertEqual(sale.delivery_fee, 500)
        self.assertEqual(sale.add_expenses, 0)
        self.assertEqual(sale.client, 'Баярма')
        self.assertEqual(sale.rama_total_cash, 7200 + 19010 + 14112)
        self.assertEqual(sale.selling_total_cash, 7500 + 19010 + 15443)

        self.assertEqual(round(sale.seller_fee), 1631)
        self.assertEqual(sale.kladman_fee, 391)
        self.assertEqual(sale.loader_fee, round((0.6 + 1.296 + 2.016) * 100))