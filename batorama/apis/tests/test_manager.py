# -*- coding: utf-8 -*-
import datetime
from django.contrib.auth.models import User

from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from stock.models import Shift, Lumber, LumberRecord, Rama
from rawstock.models import Timber, TimberRecord, IncomeTimber, Quota
import stock.testing_utils as lumber_testing
import rawstock.testing_utils as timber_testing


class SaleViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        lumber_testing.create_test_data()

        self.ramshik1 = User.objects.get(username='ramshik1')
        self.ramshik2 = User.objects.get(username='ramshik2')
        self.ramshik3 = User.objects.get(username='ramshik3')
        self.ramshik4 = User.objects.get(username='ramshik4')

        self.seller1 = User.objects.get(username='sergei')
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
        
    def test_set_lumber_cost(self):
        self.client.force_authenticate(user=self.ramshik1)
        response = self.client.post('/api/manager/stock/set_price/', 
            {
                'lumber': self.brus1.pk,
                'market_cost': 90
            },
            format='json')
        

        self.assertEqual(response.status_code, 200)
        self.brus1.refresh_from_db()
        self.assertEqual(self.brus1.market_cost, 90)



class IncomeTimberViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        lumber_testing.create_test_data()
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

        self.brus1 = Lumber.objects.filter(name__contains='брус')[0]
        self.brus2 = Lumber.objects.filter(name__contains='брус')[1]
        self.doska1 = Lumber.objects.filter(name__contains='доска')[0]
        self.doska2 = Lumber.objects.filter(name__contains='доска')[1]

        self.rama = Rama.objects.all().first()

    def test_create_api(self):
        self.client.force_authenticate(user=self.ramshik1)
        response = self.client.post('/api/manager/rawstock/timber/create_income/', 
            {
            'raw_timber_records': [
                {'timber': self.pine_timber20.pk, 'quantity': 20 },
                {'timber': self.pine_timber22.pk, 'quantity': 25 },
                {'timber': self.pine_timber28.pk, 'quantity': 30 },
            ],
            },
            format='json')

        self.assertEqual(response.status_code, 200)