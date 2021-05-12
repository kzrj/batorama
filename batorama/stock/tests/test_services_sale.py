# -*- coding: utf-8 -*-
import datetime
from django.test import TestCase, TransactionTestCase
from django.contrib.auth.models import User

from stock.models import Shift, Lumber, LumberRecord, Sale, Rama
from accounts.models import Account

import stock.testing_utils as testing


class SaleServisesTest(TransactionTestCase):
    def setUp(self):
        testing.create_test_data()

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

        self.rama = Rama.objects.all().first()

    def test_create_sale_schema1(self):
        data_list = {
            'lumbers': [
                {'lumber': self.brus1, 'quantity': 10, 'rama_price': 12000, 'selling_price': 12500,
                    'selling_total_cash': 12510},
                {'lumber': self.brus2, 'quantity': 15, 'rama_price': 12000, 'selling_price': 12800,
                    'selling_total_cash': 7680},
                {'lumber': self.doska1, 'quantity': 70, 'rama_price': 7000, 'selling_price': 7500,
                    'selling_total_cash': 15120},
                {'lumber': self.doska2, 'quantity': 55, 'rama_price': 7000, 'selling_price': 7200,
                    'selling_total_cash': 9504},
            ],
            'is_person': True,
            'is_organization': False,
            'loader': True,
            'seller': self.seller1,
            'kladman': self.kladman,
            'delivery_fee': 0,
            'add_expenses': 0,
            'note': 'Sodbo'
        }
            
        sale = Sale.objects.create_sale_schema1(
            raw_records=data_list['lumbers'],
            initiator=self.kladman,
            seller=data_list['seller'],
            bonus_kladman=data_list['kladman'],
            loader=data_list['loader'],
            delivery_fee=data_list['delivery_fee'],
            add_expenses=data_list['add_expenses'],
            note=data_list['note'],
            )

        self.assertEqual(sale.volume, round(0.6 + 0.6 + 2.016 + 1.32, 4))
        self.assertEqual(sale.seller, self.seller1)
        self.assertEqual(sale.bonus_kladman, self.kladman)
        self.assertEqual(sale.delivery_fee, 0)
        self.assertEqual(sale.add_expenses, 0)
        self.assertEqual(sale.note, 'Sodbo')
        self.assertEqual(sale.rama_total_cash, 7200 + 7200 + 14112 + 9240)
        self.assertEqual(sale.selling_total_cash, 44814)

        self.assertEqual(sale.seller_fee, 44814 - (7200 + 7200 + 14112 + 9240))
        self.assertEqual(sale.kladman_fee, round((0.6 + 0.6 + 2.016 + 1.32) * 100))
        self.assertEqual(sale.loader_fee, round((0.6 + 0.6 + 2.016 + 1.32) * 100))

        self.assertEqual(sale.net_rama_cash, 
            sale.rama_total_cash - sale.kladman_fee - sale.loader_fee - sale.delivery_fee)

    def test_create_sale_schema1_2(self):
        # without kladman bonus
        data_list = {
            'lumbers': [
                {'lumber': self.brus1, 'quantity': 10, 'rama_price': 12000, 'selling_price': 12500,
                    'selling_total_cash': 12510},
                {'lumber': self.brus2, 'quantity': 15, 'rama_price': 12000, 'selling_price': 12800,
                    'selling_total_cash': 7680},
                {'lumber': self.doska1, 'quantity': 70, 'rama_price': 7000, 'selling_price': 7500,
                    'selling_total_cash': 15120},
                {'lumber': self.doska2, 'quantity': 55, 'rama_price': 7000, 'selling_price': 7200,
                    'selling_total_cash': 9504},
            ],
            'is_person': True,
            'is_organization': False,
            'loader': True,
            'seller': self.seller1,
            'kladman': None,
            'delivery_fee': 0,
            'add_expenses': 0,
            'note': 'Sodbo'
        }
            
        sale = Sale.objects.create_sale_schema1(
            raw_records=data_list['lumbers'],
            initiator=self.kladman,
            seller=data_list['seller'],
            bonus_kladman=data_list['kladman'],
            loader=data_list['loader'],
            delivery_fee=data_list['delivery_fee'],
            add_expenses=data_list['add_expenses'],
            note=data_list['note'],
            )

        self.assertEqual(sale.volume, round(0.6 + 0.6 + 2.016 + 1.32, 4))
        self.assertEqual(sale.seller, self.seller1)
        self.assertEqual(sale.bonus_kladman, None)
        self.assertEqual(sale.delivery_fee, 0)
        self.assertEqual(sale.add_expenses, 0)
        self.assertEqual(sale.note, 'Sodbo')
        self.assertEqual(sale.rama_total_cash, 7200 + 7200 + 14112 + 9240)
        self.assertEqual(sale.selling_total_cash, 44814)

        self.assertEqual(sale.seller_fee, 44814 - (7200 + 7200 + 14112 + 9240))
        self.assertEqual(sale.kladman_fee, 0)
        self.assertEqual(sale.loader_fee, round((0.6 + 0.6 + 2.016 + 1.32) * 100))

        self.assertEqual(sale.net_rama_cash, 
            sale.rama_total_cash - sale.kladman_fee - sale.loader_fee - sale.delivery_fee)

    def test_create_sale_schema1_2(self):
        # without seller bonus, minus delivery
        data_list = {
            'lumbers': [
                {'lumber': self.brus1, 'quantity': 10, 'rama_price': 12000, 'selling_price': 12000,
                    'selling_total_cash': 7200},
                {'lumber': self.brus2, 'quantity': 15, 'rama_price': 12000, 'selling_price': 12000,
                    'selling_total_cash': 7200},
                {'lumber': self.doska1, 'quantity': 70, 'rama_price': 7000, 'selling_price': 7000,
                    'selling_total_cash': 14112},
                {'lumber': self.doska2, 'quantity': 55, 'rama_price': 7000, 'selling_price': 7000,
                    'selling_total_cash': 9240},
            ],
            'is_person': True,
            'is_organization': False,
            'loader': True,
            'seller': None,
            'kladman': None,
            'delivery_fee': 500,
            'add_expenses': 0,
            'note': 'Sodbo'
        }
            
        sale = Sale.objects.create_sale_schema1(
            raw_records=data_list['lumbers'],
            initiator=self.kladman,
            seller=data_list['seller'],
            bonus_kladman=data_list['kladman'],
            loader=data_list['loader'],
            delivery_fee=data_list['delivery_fee'],
            add_expenses=data_list['add_expenses'],
            note=data_list['note'],
            )

        self.assertEqual(sale.volume, round(0.6 + 0.6 + 2.016 + 1.32, 4))
        self.assertEqual(sale.seller, None)
        self.assertEqual(sale.bonus_kladman, None)
        self.assertEqual(sale.delivery_fee, 500)
        self.assertEqual(sale.add_expenses, 0)
        self.assertEqual(sale.note, 'Sodbo')
        self.assertEqual(sale.rama_total_cash, 7200 + 7200 + 14112 + 9240)
        self.assertEqual(sale.selling_total_cash, 7200 + 7200 + 14112 + 9240)

        self.assertEqual(sale.seller_fee, 0)
        self.assertEqual(sale.kladman_fee, 0)
        self.assertEqual(sale.loader_fee, round((0.6 + 0.6 + 2.016 + 1.32) * 100))

        self.assertEqual(sale.net_rama_cash,
         sale.rama_total_cash - sale.kladman_fee - sale.loader_fee - sale.delivery_fee)

    def test_create_sale_china(self):
        data_list = {
            'lumbers': [
                {'lumber': self.china_brus1, 'quantity': 10, 'rama_price': 15000,
                 'selling_price': 15000, 'selling_total_cash': 19010},
                {'lumber': self.china_brus2, 'quantity': 15, 'rama_price': 15000,
                 'selling_price': 15000, 'selling_total_cash': 23709},
            ],
            'loader': False,
            'delivery_fee': 500,
            'add_expenses': 0,
            'note': 'China'
        }
            
        sale = Sale.objects.create_sale_china(
            raw_records=data_list['lumbers'],
            initiator=self.kladman,
            loader=data_list['loader'],
            delivery_fee=data_list['delivery_fee'],
            add_expenses=data_list['add_expenses'],
            note=data_list['note'],
            )

        self.assertEqual(sale.volume, round(1.26736 + 1.58064, 4))
        self.assertEqual(sale.seller, None)
        self.assertEqual(sale.bonus_kladman, None)
        self.assertEqual(sale.delivery_fee, 500)
        self.assertEqual(sale.add_expenses, 0)
        self.assertEqual(sale.note, 'China')
        self.assertEqual(sale.rama_total_cash, 19010 + 23710)
        self.assertEqual(sale.selling_total_cash, 19010 + 23709)

        self.assertEqual(sale.seller_fee, 0)
        self.assertEqual(sale.kladman_fee, 0)
        self.assertEqual(sale.loader_fee, 0)

        self.assertEqual(sale.net_rama_cash,
         sale.rama_total_cash - sale.kladman_fee - sale.loader_fee - sale.delivery_fee)