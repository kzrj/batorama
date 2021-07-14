# -*- coding: utf-8 -*-
import datetime
from django.contrib.auth.models import User

from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from stock.models import Shift, Lumber, LumberRecord, Rama, Sale, ReSaw
from rawstock.models import Timber, TimberRecord, IncomeTimber, Quota
from cash.models import CashRecord
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



# class IncomeTimberViewSetTest(APITestCase):
#     def setUp(self):
#         self.client = APIClient()
#         lumber_testing.create_test_data()
#         timber_testing.create_test_timber()

#         self.seller1 = User.objects.get(username='seller1')
#         self.kladman = User.objects.get(username='kladman')

#         self.ramshik1 = User.objects.get(username='ramshik1')
#         self.ramshik2 = User.objects.get(username='ramshik2')
#         self.ramshik3 = User.objects.get(username='ramshik3')
#         self.ramshik4 = User.objects.get(username='ramshik4')

#         self.pine_timber20 = Timber.objects.get(diameter=20, wood_species='pine')
#         self.pine_timber22 = Timber.objects.get(diameter=22, wood_species='pine')
#         self.pine_timber28 = Timber.objects.get(diameter=28, wood_species='pine')

#         self.brus1 = Lumber.objects.filter(name__contains='брус')[0]
#         self.brus2 = Lumber.objects.filter(name__contains='брус')[1]
#         self.doska1 = Lumber.objects.filter(name__contains='доска')[0]
#         self.doska2 = Lumber.objects.filter(name__contains='доска')[1]

#         self.rama = Rama.objects.all().first()

#     def test_create_api(self):
#         self.client.force_authenticate(user=self.ramshik1)
#         response = self.client.post('/api/manager/rawstock/timber/create_income/', 
#             {
#             'raw_timber_records': [
#                 {'timber': self.pine_timber20.pk, 'quantity': 20 },
#                 {'timber': self.pine_timber22.pk, 'quantity': 25 },
#                 {'timber': self.pine_timber28.pk, 'quantity': 30 },
#             ],
#             },
#             format='json')

#         self.assertEqual(response.status_code, 200)


class ShiftViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        lumber_testing.create_test_data()

        self.rama = Rama.objects.all().first()
        self.rama2 = Rama.objects.filter(name='rama2').first()

        self.ramshik1 = User.objects.get(username='ramshik1')
        self.ramshik2 = User.objects.get(username='ramshik2')
        self.ramshik3 = User.objects.get(username='ramshik3')
        self.ramshik4 = User.objects.get(username='ramshik4')

        self.brus1 = Lumber.objects.filter(name__contains='брус')[0]
        self.brus2 = Lumber.objects.filter(name__contains='брус')[1]
        self.doska1 = Lumber.objects.filter(name__contains='доска')[0]
        self.doska2 = Lumber.objects.filter(name__contains='доска')[1]

        self.manager1 = User.objects.get(username='manager1')
        self.manager1.account.can_see_rama_shift.add(self.rama)

        self.manager2 = User.objects.get(username='manager2')
        self.manager2.account.can_see_rama_shift.add(self.rama2)

    def test_shift_create_init_data(self):
        self.client.force_authenticate(user=self.manager1)
        response = self.client.get('/api/manager/shifts/create/init_data/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data['lumbers']) > 0)
        
    def test_shift_create(self):
        self.client.force_authenticate(user=self.manager1)
        response = self.client.post('/api/manager/shifts/create/', 
            {
            # 'date': '2021-04-09',
            'raw_records':[
                {'lumber': self.brus1.pk, 'quantity': 10, 'volume_total': 0.6, 'employee_rate': 600,
                 'cash': 360,  },
                {'lumber': self.brus2.pk, 'quantity': 10, 'volume_total': 0.4, 'employee_rate': 600,
                 'cash': 240 },
                {'lumber': self.doska1.pk, 'quantity': 50, 'volume_total': 1.44, 'employee_rate': 600,
                'cash': 864 },
                {'lumber': self.doska2.pk, 'quantity': 40, 'volume_total': 0.96, 'employee_rate': 600,
                 'cash': 576 },
            ],
            'shift_type': 'day',
            'employees': [self.ramshik1.account.pk, self.ramshik2.account.pk, self.ramshik3.account.pk,],
            'employee_cash': 1000,
            'volume': 1000,

            }, format='json')
        self.assertEqual(response.status_code, 201)

    def test_permissions(self):
        self.client.force_authenticate(user=self.ramshik1)
        response = self.client.get('/api/manager/shifts/create/init_data/')
        self.assertEqual(response.status_code, 403)


class SaleViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        lumber_testing.create_test_data()

        self.rama = Rama.objects.all().first()
        self.rama2 = Rama.objects.filter(name='rama2').first()

        self.ramshik1 = User.objects.get(username='ramshik1')
        self.ramshik2 = User.objects.get(username='ramshik2')

        self.seller1 = User.objects.get(username='seller1')
        self.kladman = User.objects.get(username='kladman')

        self.manager1 = User.objects.get(username='manager1')
        self.manager2 = User.objects.get(username='manager2')

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
        
    def test_sale_create(self):
        self.client.force_authenticate(user=self.manager1)
        response = self.client.post('/api/manager/sales/create/', 
            {
            'raw_records': [
                {'lumber': self.brus1.pk, 'quantity': 10, 'rama_price': 12000, 'selling_price': 12500,
                    'selling_total_cash': 7500, 'calc_type': 'exact'},
                {'lumber': self.china_brus1.pk, 'quantity': 10, 'rama_price': 15000,
                    'selling_price': 15000, 'selling_total_cash': 19010, 'calc_type': 'china'},
                {'lumber': self.doska4_18.pk, 'quantity': 70, 'rama_price': 7000, 'selling_price': 7500,
                    'selling_total_cash': 15443, 'calc_type': 'round'},
            ],
            'loader': True,
            'seller': self.seller1.pk,
            'bonus_kladman': self.kladman.pk,
            'delivery_fee': 500,
            'add_expenses': 0,
            'note': '',
            'client': 'Баярма'
        }, format='json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['sale']['lumber_records'][0]['quantity'], 10)

    def test_sale_delete(self):
        self.client.force_authenticate(user=self.manager1)
        response = self.client.post('/api/manager/sales/create/', 
            {
            'raw_records': [
                {'lumber': self.brus1.pk, 'quantity': 10, 'rama_price': 12000, 'selling_price': 12500,
                    'selling_total_cash': 7500, 'calc_type': 'exact'},
                {'lumber': self.china_brus1.pk, 'quantity': 10, 'rama_price': 15000,
                    'selling_price': 15000, 'selling_total_cash': 19010, 'calc_type': 'china'},
                {'lumber': self.doska4_18.pk, 'quantity': 70, 'rama_price': 7000, 'selling_price': 7500,
                    'selling_total_cash': 15443, 'calc_type': 'round'},
            ],
            'loader': True,
            'seller': self.seller1.pk,
            'bonus_kladman': self.kladman.pk,
            'delivery_fee': 500,
            'add_expenses': 0,
            'note': '',
            'client': 'Баярма'
        }, format='json')
        
        sale = Sale.objects.all().first()

        response = self.client.delete(f'/api/manager/sales/{sale.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Sale.objects.all().count(), 0)

    def test_permissions(self):
        self.client.force_authenticate(user=self.ramshik1)
        response = self.client.post('/api/manager/sales/create/', 
            {
            'raw_records': [
                {'lumber': self.brus1.pk, 'quantity': 10, 'rama_price': 12000, 'selling_price': 12500,
                    'selling_total_cash': 7500, 'calc_type': 'exact'},
                {'lumber': self.china_brus1.pk, 'quantity': 10, 'rama_price': 15000,
                    'selling_price': 15000, 'selling_total_cash': 19010, 'calc_type': 'china'},
                {'lumber': self.doska4_18.pk, 'quantity': 70, 'rama_price': 7000, 'selling_price': 7500,
                    'selling_total_cash': 15443, 'calc_type': 'round'},
            ],
            'loader': True,
            'seller': self.seller1.pk,
            'bonus_kladman': self.kladman.pk,
            'delivery_fee': 500,
            'add_expenses': 0,
            'note': '',
            'client': 'Баярма'
        }, format='json')

        self.assertEqual(response.status_code, 403)
        self.client.logout()

        self.client.force_authenticate(user=self.manager1)
        response = self.client.post('/api/manager/sales/create/', 
            {
            'raw_records': [
                {'lumber': self.brus1.pk, 'quantity': 10, 'rama_price': 12000, 'selling_price': 12500,
                    'selling_total_cash': 7500, 'calc_type': 'exact'},
                {'lumber': self.china_brus1.pk, 'quantity': 10, 'rama_price': 15000,
                    'selling_price': 15000, 'selling_total_cash': 19010, 'calc_type': 'china'},
                {'lumber': self.doska4_18.pk, 'quantity': 70, 'rama_price': 7000, 'selling_price': 7500,
                    'selling_total_cash': 15443, 'calc_type': 'round'},
            ],
            'loader': True,
            'seller': self.seller1.pk,
            'bonus_kladman': self.kladman.pk,
            'delivery_fee': 500,
            'add_expenses': 0,
            'note': '',
            'client': 'Баярма'
        }, format='json')
        self.client.logout()
        
        sale = Sale.objects.all().first()

        self.client.force_authenticate(user=self.manager2)
        response = self.client.delete(f'/api/manager/sales/{sale.pk}/')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Sale.objects.all().count(), 1)
        self.client.logout()

    def test_sale_create_data(self):
        self.client.force_authenticate(user=self.ramshik1)
        response = self.client.get('/api/manager/sales/create/init_data/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['kladman_id'], self.kladman.pk)


class CashRecordViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        lumber_testing.create_test_data()

        self.rama = Rama.objects.all().first()
        self.rama2 = Rama.objects.filter(name='rama2').first()

        self.ramshik1 = User.objects.get(username='ramshik1')

        self.manager1 = User.objects.get(username='manager1')
        self.manager2 = User.objects.get(username='manager2')

    def test_create_cash_record(self):
        self.client.force_authenticate(user=self.manager1)
        response = self.client.post('/api/manager/cash_records/create_expense/', 
            {'amount': 999, 'note': 'test'})
        self.assertEqual(response.data['expense']['amount'], 999)

        response = self.client.get('/api/manager/cash_records/list/')
        self.assertEqual(response.data['count'], 1)
        self.client.logout()

        self.client.force_authenticate(user=self.manager2)
        response = self.client.get('/api/manager/cash_records/list/')
        self.assertEqual(response.data['count'], 0)
        self.client.logout()

        self.client.force_authenticate(user=self.manager1)
        cash_record = CashRecord.objects.all().first()
        response = self.client.delete(f'/api/manager/cash_records/{cash_record.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['records']), 0)

    def test_permissions(self):
        self.client.force_authenticate(user=self.manager1)
        response = self.client.post('/api/manager/cash_records/create_expense/', 
            {'amount': 999, 'note': 'test'})
        self.assertEqual(response.data['expense']['amount'], 999)
        self.client.logout()

        self.client.force_authenticate(user=self.manager2)
        cash_record = CashRecord.objects.all().first()
        response = self.client.delete(f'/api/manager/cash_records/{cash_record.pk}/')
        self.assertEqual(response.status_code, 404)
        self.client.logout()

        self.client.force_authenticate(user=self.ramshik1)
        response = self.client.post('/api/manager/cash_records/create_expense/', 
            {'amount': 999, 'note': 'test'})
        self.assertEqual(response.status_code, 403)
        self.client.logout()


class ResawViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        lumber_testing.create_test_data()

        self.rama = Rama.objects.all().first()
        self.rama2 = Rama.objects.filter(name='rama2').first()

        self.ramshik1 = User.objects.get(username='ramshik1')
        self.ramshik2 = User.objects.get(username='ramshik2')
        self.ramshik3 = User.objects.get(username='ramshik3')
        self.ramshik4 = User.objects.get(username='ramshik4')

        self.brus1 = Lumber.objects.filter(name__contains='брус')[0]
        self.brus2 = Lumber.objects.filter(name__contains='брус')[1]
        self.doska1 = Lumber.objects.filter(name__contains='доска')[0]
        self.doska2 = Lumber.objects.filter(name__contains='доска')[1]

        self.manager1 = User.objects.get(username='manager1')
        self.manager1.account.can_see_rama_resaws.add(self.rama)

        self.manager2 = User.objects.get(username='manager2')
        self.manager2.account.can_see_rama_resaws.add(self.rama2)

    def test_resaw_create(self):
        self.client.force_authenticate(user=self.manager1)
        response = self.client.post('/api/manager/resaws/create/', 
            {
                'lumber_in': self.brus1.pk,
                'lumber_in_quantity': 10,
                'lumber_out': self.brus2.pk,
                'lumber_out_quantity': 15,
            }, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['created']['lumber_in_quantity'], 10)
        self.assertEqual(response.data['created']['lumber_out_quantity'], 15)

    def test_resaw_delete(self):
        self.client.force_authenticate(user=self.manager1)
        response = self.client.post('/api/manager/resaws/create/', 
            {
                'lumber_in': self.brus1.pk,
                'lumber_in_quantity': 10,
                'lumber_out': self.brus2.pk,
                'lumber_out_quantity': 15,
            }, format='json')

        resaw = ReSaw.objects.all().first()
        response = self.client.delete(f'/api/manager/resaws/{resaw.pk}/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['resaws']), 0)

    def test_permissions(self):
        self.client.force_authenticate(user=self.ramshik1)
        response = self.client.post('/api/manager/resaws/create/', 
            {
                'lumber_in': self.brus1.pk,
                'lumber_in_quantity': 10,
                'lumber_out': self.brus2.pk,
                'lumber_out_quantity': 15,
            }, format='json')
        self.assertEqual(response.status_code, 403)