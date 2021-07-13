# -*- coding: utf-8 -*-
import datetime
from django.contrib.auth.models import User

from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from stock.models import Shift, Lumber, LumberRecord, Rama
from rawstock.models import Timber, TimberRecord, IncomeTimber, Quota
import stock.testing_utils as lumber_testing
import rawstock.testing_utils as timber_testing


class ShiftListViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        lumber_testing.create_test_data()

        self.rama = Rama.objects.all().first()
        self.rama2 = Rama.objects.filter(name='rama2').first()

        self.ramshik1 = User.objects.get(username='ramshik1')
        self.ramshik2 = User.objects.get(username='ramshik2')
        self.ramshik3 = User.objects.get(username='ramshik3')
        self.ramshik4 = User.objects.get(username='ramshik4')

        self.seller1 = User.objects.get(username='sergei')
        self.seller1.account.can_see_rama_stock.add(self.rama, self.rama2)
        self.seller2 = User.objects.get(username='seller1')
        self.seller2.account.can_see_rama_stock.add(self.rama2)
        self.kladman = User.objects.get(username='kladman')

        self.manager1 = User.objects.get(username='manager1')
        self.manager1.account.can_see_rama_shift.add(self.rama)

        self.manager2 = User.objects.get(username='manager2')
        self.manager2.account.can_see_rama_shift.add(self.rama2)

        self.capo1 = User.objects.get(username='capo1')
        self.capo1.account.can_see_rama_shift.add(self.rama, self.rama2)

        self.brus1 = Lumber.objects.filter(name__contains='брус')[0]
        self.brus2 = Lumber.objects.filter(name__contains='брус')[1]
        self.doska1 = Lumber.objects.filter(name__contains='доска')[0]
        self.doska2 = Lumber.objects.filter(name__contains='доска')[1]

        self.doska4_18 = Lumber.objects.filter(name__contains='доска 4*18',
             wood_species='pine')[0]
        self.doska25_18 = Lumber.objects.filter(name__contains='доска 2.5*18',
             wood_species='pine')[0]

        self.china_brus1 = Lumber.objects.filter(name='брус 18*18', wood_species='pine',
         china_volume__isnull=False).first()
        self.china_brus2 = Lumber.objects.filter(name='брус 15*18', wood_species='pine',
         china_volume__isnull=False).first()

        employees = [self.ramshik1.account, self.ramshik2.account]
        data_list = [
            {'lumber': self.brus1, 'quantity': 10, 'volume_total': 0.6, 'rate': 600, 'cash': 360 },
            {'lumber': self.brus2, 'quantity': 10, 'volume_total': 0.4, 'rate': 600, 'cash': 240 },
            {'lumber': self.doska4_18, 'quantity': 50, 'volume_total': 1.44, 'rate': 600, 'cash': 864 },
            {'lumber': self.doska25_18, 'quantity': 40, 'volume_total': 0.96, 'rate': 600, 'cash': 576 },
        ]

        shift = Shift.objects.create_shift_raw_records(shift_type='day', employees=employees, 
            raw_records=data_list, cash=1200, initiator=self.manager1, rama=self.rama)
        
    def test_get_rama_shifts(self):
        self.client.force_authenticate(user=self.ramshik1)
        response = self.client.get(f'/api/ramshik/shifts/list/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)
        self.client.logout()

        self.client.force_authenticate(user=self.ramshik3)
        response = self.client.get(f'/api/ramshik/shifts/list/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 0)
        self.client.logout()

    def test_payouts_list(self):
        self.client.force_authenticate(user=self.ramshik1)
        response = self.client.get(f'/api/ramshik/payouts/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['last_payouts']), 1)
        self.client.logout()

        self.client.force_authenticate(user=self.ramshik3)
        response = self.client.get(f'/api/ramshik/payouts/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['last_payouts']), 0)
        self.client.logout()