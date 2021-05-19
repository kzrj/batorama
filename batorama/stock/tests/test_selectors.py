# -*- coding: utf-8 -*-
import datetime
from django.test import TestCase, TransactionTestCase
from django.contrib.auth.models import User
from django.db.models import Q, Subquery, OuterRef, Count, Prefetch, F, Sum

from stock.models import Shift, Lumber, LumberRecord, Sale, Rama
from accounts.models import Account

import stock.testing_utils as testing


# class StockSelectorsTest(TransactionTestCase):
#     def setUp(self):
#         testing.create_test_data()

#         self.ramshik1 = User.objects.get(username='ramshik1')
#         self.ramshik2 = User.objects.get(username='ramshik2')
#         self.ramshik3 = User.objects.get(username='ramshik3')
#         self.ramshik4 = User.objects.get(username='ramshik4')

#         self.brus1 = Lumber.objects.filter(name__contains='брус')[0]
#         self.brus2 = Lumber.objects.filter(name__contains='брус')[1]
#         self.doska1 = Lumber.objects.filter(name__contains='доска')[0]
#         self.doska2 = Lumber.objects.filter(name__contains='доска')[1]
#         self.doska3 = Lumber.objects.filter(name__contains='доска')[2]

#         self.rama = Rama.objects.all().first()

#     def test_calc_total_income_volume_by_rama_by_lumber(self):
#         employees = [self.ramshik1.account, self.ramshik2.account, self.ramshik3.account]
#         shift_data_list = [
#          {'lumber': self.brus1, 'quantity': 10, 'volume_total': 0.6, 'rate': 600, 'cash': 360 },
#          {'lumber': self.brus2, 'quantity': 10, 'volume_total': 0.4, 'rate': 600, 'cash': 240 },
#          {'lumber': self.doska1, 'quantity': 50, 'volume_total': 1.44, 'rate': 600, 'cash': 864 },
#          {'lumber': self.doska2, 'quantity': 40, 'volume_total': 0.96, 'rate': 600, 'cash': 576 },
#          {'lumber': self.doska2, 'quantity': 40, 'volume_total': 0.96, 'rate': 600, 'cash': 576 },
#          {'lumber': self.doska3, 'quantity': 40, 'volume_total': 0.96, 'rate': 600, 'cash': 576 },
#         ]

#         shift = Shift.objects.create_shift_raw_records(shift_type='day', employees=employees, 
#             raw_records=shift_data_list, cash=1200, volume=10, initiator=self.ramshik1, 
#             rama=self.rama)

#         total_income_volume = LumberRecord.objects.calc_total_income_volume_by_rama_by_lumber(
#             lumber=self.brus1, rama=self.rama)[0]['total_income_volume']

#         self.assertEqual(total_income_volume, 0.6)

#     def test_calc_total_outcome_volume_by_rama_by_lumber(self):
#         sale_data_list = [
#          {'lumber': self.brus1, 'quantity': 10, 'volume_total': 0.6, 'rate': 12000, 'cash': 7200 },
#          {'lumber': self.brus2, 'quantity': 10, 'volume_total': 0.4, 'rate': 11000, 'cash': 4400 },
#          {'lumber': self.doska1, 'quantity': 50, 'volume_total': 1.44, 'rate': 7500, 'cash': 10800 },
#          {'lumber': self.doska2, 'quantity': 40, 'volume_total': 0.96, 'rate': 7000, 'cash': 6720 },
#         ]

#         sale = Sale.objects.create_sale_raw_records(raw_records=sale_data_list, cash=1000,
#          volume=10, initiator=self.ramshik1, rama=self.rama)

#         total_outcome_volume = LumberRecord.objects.calc_total_outcome_volume_by_rama_by_lumber(
#             lumber=self.brus1, rama=self.rama)[0]['total_outcome_volume']

#         self.assertEqual(total_outcome_volume, 0.6)

#     def test_lumber_add_rama_current_stock(self):
#         employees = [self.ramshik1.account, self.ramshik2.account, self.ramshik3.account]
#         shift_data_list = [
#          {'lumber': self.brus1, 'quantity': 10, 'volume_total': 0.6, 'rate': 600, 'cash': 360 },
#          {'lumber': self.brus2, 'quantity': 10, 'volume_total': 0.4, 'rate': 600, 'cash': 240 },
#          {'lumber': self.doska1, 'quantity': 50, 'volume_total': 1.44, 'rate': 600, 'cash': 864 },
#          {'lumber': self.doska2, 'quantity': 40, 'volume_total': 0.96, 'rate': 600, 'cash': 576 },
#          {'lumber': self.doska2, 'quantity': 40, 'volume_total': 0.96, 'rate': 600, 'cash': 576 },
#          {'lumber': self.doska3, 'quantity': 40, 'volume_total': 0.96, 'rate': 600, 'cash': 576 },
#         ]

#         shift = Shift.objects.create_shift_raw_records(shift_type='day', employees=employees, 
#             raw_records=shift_data_list, cash=1200, volume=10, initiator=self.ramshik1, 
#             rama=self.rama)

#         sale_data_list = [
#          {'lumber': self.brus1, 'quantity': 10, 'volume_total': 0.6, 'rate': 12000, 'cash': 7200 },
#          {'lumber': self.brus2, 'quantity': 10, 'volume_total': 0.4, 'rate': 11000, 'cash': 4400 },
#          {'lumber': self.doska1, 'quantity': 50, 'volume_total': 1.44, 'rate': 7500, 'cash': 10800 },
#          {'lumber': self.doska2, 'quantity': 40, 'volume_total': 0.96, 'rate': 7000, 'cash': 6720 },
#         ]

#         sale = Sale.objects.create_sale_common(raw_records=sale_data_list, cash=1000,
#          volume=10, initiator=self.ramshik1, rama=self.rama)

#         lumbers = Lumber.objects.all().add_rama_current_stock(rama=self.rama)
        
#         doska2 = lumbers.get(pk=self.doska2.pk)

#         self.assertEqual(doska2.total_income_volume, 1.92)
#         self.assertEqual(doska2.total_outcome_volume, 0.96)
#         self.assertEqual(doska2.current_stock_volume, 0.96)