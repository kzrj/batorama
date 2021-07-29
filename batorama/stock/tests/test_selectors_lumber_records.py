# -*- coding: utf-8 -*-
import datetime
from django.test import TestCase, TransactionTestCase
from django.contrib.auth.models import User

from stock.models import Shift, Lumber, LumberRecord, Sale, Rama, ReSaw, RefuseLumber
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


class LumberRecordsSelectorsStockTest(TransactionTestCase):
    def setUp(self):
        testing.create_test_data()

        self.seller1 = User.objects.get(username='seller1')
        self.kladman = User.objects.get(username='kladman')
        self.ramshik1 = User.objects.get(username='ramshik1')
        self.ramshik2 = User.objects.get(username='ramshik2')
        self.ramshik3 = User.objects.get(username='ramshik3')

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

        employees = [self.ramshik1.account, self.ramshik2.account, self.ramshik3.account]
        data_list1 = [
            {'lumber': self.brus1, 'quantity': 50, 'rate': 600, 'cash': 360 },
            {'lumber': self.brus2, 'quantity': 55, 'rate': 600, 'cash': 240 },
            {'lumber': self.doska1, 'quantity': 250, 'rate': 600, 'cash': 864 },
            {'lumber': self.doska2, 'quantity': 240, 'rate': 600, 'cash': 576 },
        ]

        self.shift = Shift.objects.create_shift_raw_records(shift_type='day', employees=employees, 
            raw_records=data_list1, cash=1200, initiator=self.ramshik1, rama=self.rama)

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

        self.sale = Sale.objects.create_sale_common(
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

        self.resaw = ReSaw.objects.create_resaw(
            resaw_lumber_in={'lumber': self.brus1, 'quantity': 10},
            resaw_lumber_out={'lumber': self.doska1, 'quantity': 44},
            rama=self.rama
           )

        self.refuse = RefuseLumber.objects.create_refuse(
            lumber=self.brus1, quantity=2, rama=self.rama)

    def test_calc_total_income_outcome_quantity_by_rama_by_lumber(self):
        income_lumber_records_brus1 = LumberRecord.objects.calc_total_income_quantity_by_rama_by_lumber(
            lumber=self.brus1, rama=self.rama)
        outcome_lumber_records_brus1 = LumberRecord.objects.calc_total_outcome_quantity_by_rama_by_lumber(
            lumber=self.brus1, rama=self.rama)
        
        self.assertEqual(income_lumber_records_brus1[0]['total_income_quantity'], 50)
        self.assertEqual(outcome_lumber_records_brus1[0]['total_outcome_quantity'], 22)

        income_lumber_records_doska1 = LumberRecord.objects.calc_total_income_quantity_by_rama_by_lumber(
            lumber=self.doska1, rama=self.rama)
        outcome_lumber_records_doska1 = LumberRecord.objects.calc_total_outcome_quantity_by_rama_by_lumber(
            lumber=self.doska1, rama=self.rama)
        
        self.assertEqual(income_lumber_records_doska1[0]['total_income_quantity'], 294)
        self.assertEqual(outcome_lumber_records_doska1[0]['total_outcome_quantity'], 70)

    def test_calc_total_income_outcome_volume_by_rama_by_lumber(self):
        income_lumber_records_brus1 = LumberRecord.objects.calc_total_income_volume_by_rama_by_lumber(
            lumber=self.brus1, rama=self.rama)
        outcome_lumber_records_brus1 = LumberRecord.objects.calc_total_outcome_volume_by_rama_by_lumber(
            lumber=self.brus1, rama=self.rama)
        
        self.assertEqual(income_lumber_records_brus1[0]['total_income_volume'], 3)
        self.assertEqual(outcome_lumber_records_brus1[0]['total_outcome_volume'], 1.32)

        income_lumber_records_doska1 = LumberRecord.objects.calc_total_income_volume_by_rama_by_lumber(
            lumber=self.doska1, rama=self.rama)
        outcome_lumber_records_doska1 = LumberRecord.objects.calc_total_outcome_volume_by_rama_by_lumber(
            lumber=self.doska1, rama=self.rama)
        
        self.assertEqual(income_lumber_records_doska1[0]['total_income_volume'], 8.4672)
        self.assertEqual(outcome_lumber_records_doska1[0]['total_outcome_volume'], 2.016)