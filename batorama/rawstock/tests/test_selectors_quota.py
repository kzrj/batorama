# -*- coding: utf-8 -*-
import datetime
from django.test import TestCase, TransactionTestCase
from django.contrib.auth.models import User

from stock.models import Rama, Shift, Lumber, Sale
from rawstock.models import Timber, TimberRecord, IncomeTimber, Quota

import stock.testing_utils as lumber_testing
import rawstock.testing_utils as timber_testing


class QuotaSelectorsTest(TransactionTestCase):
    def setUp(self):
        lumber_testing.create_init_data()
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

        data_list = [
            {'timber': self.pine_timber20, 'quantity': 20 },
            {'timber': self.pine_timber22, 'quantity': 25 },
            {'timber': self.pine_timber28, 'quantity': 30 },
        ]

        self.income_timber = IncomeTimber.objects.create_income_timber(
            raw_timber_records=data_list, initiator=self.kladman, rama=self.rama)

        data_list2 = {
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

        data_list3 = {
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
            raw_records=data_list3['lumbers'],
            initiator=self.kladman,
            loader=data_list3['loader'],
            delivery_fee=data_list3['delivery_fee'],
            add_expenses=data_list3['add_expenses'],
            note=data_list3['note'],
            client=data_list3['client'],
            seller=data_list3['seller'],
            bonus_kladman=data_list3['bonus_kladman']
            )

    def test_current_quota(self):
        pine_quota = Quota.objects.create_quota(income_timber=self.income_timber)['pine_quota']
        larch_quota = Quota.objects.create_quota(income_timber=self.income_timber)['larch_quota']
        
        self.assertEqual(pine_quota.volume_quota_brus, 8.045)
        self.assertEqual(pine_quota.volume_quota_doska, 3.218)

        sold_volumes = Sale.objects.calc_sold_volume_for_quota_calc()
        self.assertEqual(sold_volumes['total_brus_volume'], 3.324)
        self.assertEqual(sold_volumes['total_doska_volume'], 2.016)

        # self.assertEqual(pine_quota.current_quota(), (8.045 - 3.324, 3.218 - 2.016))
        self.assertEqual(larch_quota, None)