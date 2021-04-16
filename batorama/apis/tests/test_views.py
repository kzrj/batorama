# -*- coding: utf-8 -*-
import datetime
from django.contrib.auth.models import User

from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from stock.models import Shift, Lumber, LumberRecord
import stock.testing_utils as testing


class ShiftViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        testing.create_test_data()

        self.ramshik1 = User.objects.get(username='ramshik1')
        self.ramshik2 = User.objects.get(username='ramshik2')
        self.ramshik3 = User.objects.get(username='ramshik3')
        self.ramshik4 = User.objects.get(username='ramshik4')

        self.brus1 = Lumber.objects.filter(name__contains='брус')[0]
        self.brus2 = Lumber.objects.filter(name__contains='брус')[1]
        self.doska1 = Lumber.objects.filter(name__contains='доска')[0]
        self.doska2 = Lumber.objects.filter(name__contains='доска')[1]
        
    def test_shift_create(self):
        self.client.force_authenticate(user=self.ramshik1)
        response = self.client.post('/api/shifts/', 
            {
            # 'date': '2021-04-09',
            'raw_records':[
                {'lumber': self.brus1.pk, 'quantity': 10, 'volume': 0.6, 'employee_rate': 600, 'total': 360 },
                {'lumber': self.brus2.pk, 'quantity': 10, 'volume': 0.4, 'employee_rate': 600, 'total': 240 },
                {'lumber': self.doska1.pk, 'quantity': 50, 'volume': 1.44, 'employee_rate': 600, 'total': 864 },
                {'lumber': self.doska2.pk, 'quantity': 40, 'volume': 0.96, 'employee_rate': 600, 'total': 576 },
            ],
            'shift_type': 'day',
            'employees': [self.ramshik1.employee.pk, self.ramshik2.employee.pk, self.ramshik3.employee.pk,]

            }, format='json')
        print(response.data)