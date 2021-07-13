# -*- coding: utf-8 -*-
import datetime
from django.contrib.auth.models import User

from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from stock.models import Shift, Lumber, LumberRecord, Rama, Sale
from cash.models import CashRecord

import stock.testing_utils as lumber_testing
import rawstock.testing_utils as timber_testing


class LumberStockViewTest(APITestCase):
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

        employees = [self.ramshik1.account, self.ramshik2.account, self.ramshik3.account]
        data_list = [
            {'lumber': self.brus1, 'quantity': 10, 'volume_total': 0.6, 'rate': 600, 'cash': 360 },
            {'lumber': self.brus2, 'quantity': 10, 'volume_total': 0.4, 'rate': 600, 'cash': 240 },
            {'lumber': self.doska4_18, 'quantity': 50, 'volume_total': 1.44, 'rate': 600, 'cash': 864 },
            {'lumber': self.doska25_18, 'quantity': 40, 'volume_total': 0.96, 'rate': 600, 'cash': 576 },
        ]

        shift = Shift.objects.create_shift_raw_records(shift_type='day', employees=employees, 
            raw_records=data_list, cash=1200, initiator=self.ramshik1, rama=self.rama)
        
    def test_get_rama_stock(self):
        self.client.force_authenticate(user=self.seller1)
        response = self.client.get(f'/api/common/stock/?rama={self.rama.pk}')

        for lumber in response.data['results']:
            if lumber['id'] == self.doska4_18.pk:
                self.assertEqual(lumber['current_stock_quantity'], 50)

        response = self.client.get(f'/api/common/stock/?rama={self.rama2.pk}')
        for lumber in response.data['results']:
            if lumber['id'] == self.doska4_18.pk:
                self.assertEqual(lumber['current_stock_quantity'], 0)

    def test_get_rama_stock_permissions(self):
        self.client.force_authenticate(user=self.seller2)
        response = self.client.get(f'/api/common/stock/?rama={self.rama.pk}')
        self.assertEqual(response.status_code, 403)

        response = self.client.get(f'/api/common/stock/?rama=3')
        self.assertEqual(response.status_code, 403)


class ShiftStockViewTest(APITestCase):
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

        employees = [self.ramshik1.account, self.ramshik2.account, self.ramshik3.account]
        data_list = [
            {'lumber': self.brus1, 'quantity': 10, 'volume_total': 0.6, 'rate': 600, 'cash': 360 },
            {'lumber': self.brus2, 'quantity': 10, 'volume_total': 0.4, 'rate': 600, 'cash': 240 },
            {'lumber': self.doska4_18, 'quantity': 50, 'volume_total': 1.44, 'rate': 600, 'cash': 864 },
            {'lumber': self.doska25_18, 'quantity': 40, 'volume_total': 0.96, 'rate': 600, 'cash': 576 },
        ]

        shift = Shift.objects.create_shift_raw_records(shift_type='day', employees=employees, 
            raw_records=data_list, cash=1200, initiator=self.manager1, rama=self.rama)
        
    def test_get_rama_shifts(self):
        self.client.force_authenticate(user=self.manager1)
        response = self.client.get(f'/api/common/shifts/?rama={self.rama.pk}')
        self.assertEqual(response.status_code, 200)
        self.client.logout()

        self.client.force_authenticate(user=self.capo1)
        response = self.client.get(f'/api/common/shifts/?rama={self.rama.pk}')
        self.assertEqual(response.status_code, 200)

        response = self.client.get(f'/api/common/shifts/?rama={self.rama2.pk}')
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_get_rama_shifts_permissions(self):
        self.client.force_authenticate(user=self.manager1)
        response = self.client.get(f'/api/common/shifts/?shifts={self.rama2.pk}')
        self.assertEqual(response.status_code, 403)

        response = self.client.get(f'/api/common/shifts/?rama=335')
        self.assertEqual(response.status_code, 403)
        self.client.logout()

        self.client.force_authenticate(user=self.seller1)
        response = self.client.get(f'/api/common/shifts/?shifts={self.rama2.pk}')
        self.assertEqual(response.status_code, 403)

        response = self.client.get(f'/api/common/shifts/?rama={self.rama.pk}')
        self.assertEqual(response.status_code, 403)
        self.client.logout()

    def test_get_rama_shifts_filter(self):
        self.client.force_authenticate(user=self.manager1)
        date1 = datetime.date.today()
        date2 = date1 - datetime.timedelta(days=1)
        date3 = date1 + datetime.timedelta(days=2)

        response = self.client.get(f'/api/common/shifts/?rama={self.rama.pk}&date_after=\
            {date1.strftime("%Y-%m-%d")}&date_before={date1.strftime("%Y-%m-%d")}')
        self.assertEqual(len(response.data['results']), 1)

        response = self.client.get(f'/api/common/shifts/?rama={self.rama.pk}&date_after=\
            {date3.strftime("%Y-%m-%d")}&date_before={date3.strftime("%Y-%m-%d")}')
        self.assertEqual(len(response.data['results']), 0)

        response = self.client.get(f'/api/common/shifts/?rama={self.rama.pk}&date_after=\
            {date3.strftime("%Y-%m-%d")}')
        self.assertEqual(len(response.data['results']), 0)
    

class SalesStockViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        lumber_testing.create_test_data()

        self.rama = Rama.objects.filter(name='batorama').first()
        self.rama2 = Rama.objects.filter(name='rama2').first()

        self.ramshik1 = User.objects.get(username='ramshik1')
        self.ramshik2 = User.objects.get(username='ramshik2')
        self.ramshik3 = User.objects.get(username='ramshik3')
        self.ramshik4 = User.objects.get(username='ramshik4')

        self.seller1 = User.objects.get(username='sergei')
        self.seller1.account.can_see_rama_sales.add(self.rama, self.rama2)

        self.seller2 = User.objects.get(username='seller1')
        self.seller2.account.can_see_rama_sales.add(self.rama2)

        self.kladman = User.objects.get(username='kladman')

        self.manager1 = User.objects.get(username='manager1')
        self.manager1.account.can_see_rama_sales.add(self.rama, self.rama2)

        self.manager2 = User.objects.get(username='manager2')
        self.manager2.account.can_see_rama_sales.add(self.rama2)

        self.capo1 = User.objects.get(username='capo1')
        self.capo1.account.can_see_rama_sales.add(self.rama)

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

        data_list1 = {
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
            raw_records=data_list1['lumbers'],
            initiator=self.manager1,
            loader=data_list1['loader'],
            delivery_fee=data_list1['delivery_fee'],
            add_expenses=data_list1['add_expenses'],
            note=data_list1['note'],
            client=data_list1['client'],
            seller=data_list1['seller'],
            bonus_kladman=data_list1['bonus_kladman']
            )

        data_list2 = {
            'lumbers': [
                {'lumber': self.brus1, 'quantity': 20, 'rama_price': 12000, 
                    'selling_price': 12500,'selling_total_cash': 7500, 'calc_type': 'exact'},
                {'lumber': self.doska25_18, 'quantity': 60, 'rama_price': 7000,
                    'selling_price': 7500, 'selling_total_cash': 15443, 'calc_type': 'round'},
            ],
            'loader': True,
            'seller': self.seller2,
            'bonus_kladman': None,
            'delivery_fee': 500,
            'add_expenses': 0,
            'note': '',
            'client': 'Баярма2'
        }

        self.sale2 = Sale.objects.create_sale_common(
            raw_records=data_list2['lumbers'],
            initiator=self.manager2,
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
                {'lumber': self.brus1, 'quantity': 30, 'rama_price': 12000, 'selling_price': 12500,
                    'selling_total_cash': 7500, 'calc_type': 'exact'},
                {'lumber': self.china_brus1, 'quantity': 30, 'rama_price': 15000,
                    'selling_price': 15000, 'selling_total_cash': 19010, 'calc_type': 'china'},
            ],
            'loader': True,
            'seller': self.seller2,
            'bonus_kladman': self.kladman,
            'delivery_fee': 500,
            'add_expenses': 0,
            'note': '',
            'client': 'Баярма3'
        }

        self.sale3 = Sale.objects.create_sale_common(
            raw_records=data_list3['lumbers'],
            initiator=self.manager2,
            loader=data_list3['loader'],
            delivery_fee=data_list3['delivery_fee'],
            add_expenses=data_list3['add_expenses'],
            note=data_list3['note'],
            client=data_list3['client'],
            seller=data_list3['seller'],
            bonus_kladman=data_list3['bonus_kladman']
            )
        
    def test_get_rama_sales(self):
        self.client.force_authenticate(user=self.manager1)
        response = self.client.get(f'/api/common/sales/?rama={self.rama.pk}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['sales']), 1)
        
        self.manager1.account.is_seller = True
        self.manager1.account.save()

        response = self.client.get(f'/api/common/sales/?rama={self.rama2.pk}\
            &seller={self.manager1.pk}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['sales']), 0)
        self.client.logout()

        self.client.force_authenticate(user=self.capo1)
        response = self.client.get(f'/api/common/sales/?rama={self.rama.pk}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['sales']), 1)
        self.client.logout()

    def test_get_rama_sales_filter(self):
        self.client.force_authenticate(user=self.seller2)
        response = self.client.get(f'/api/common/sales/?rama={self.rama2.pk}\
            &seller={self.seller2.pk}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['sales']), 2)
        self.client.logout()  

    def test_get_rama_sales_permissions(self):
        self.client.force_authenticate(user=self.capo1)       
        response = self.client.get(f'/api/common/sales/?rama={self.rama2.pk}')
        self.assertEqual(response.status_code, 403)
        self.client.logout()

        self.client.force_authenticate(user=self.seller2)       
        response = self.client.get(f'/api/common/sales/?rama={self.rama2.pk}')
        self.assertEqual(response.status_code, 403)
        self.client.logout()

        self.client.force_authenticate(user=self.seller2)       
        response = self.client.get(f'/api/common/sales/?rama={self.rama.pk}\
            &seller={self.seller2.pk}')
        self.assertEqual(response.status_code, 403)
        self.client.logout()

        self.client.force_authenticate(user=self.manager2)       
        response = self.client.get(f'/api/common/sales/?rama={self.rama.pk}')
        self.assertEqual(response.status_code, 403)
        self.client.logout()

        self.client.force_authenticate(user=self.manager1)       
        response = self.client.get(f'/api/common/sales/?rama={self.rama2.pk}')
        self.assertEqual(response.status_code, 403)
        self.client.logout()


class CashRecordsViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        lumber_testing.create_test_data()

        self.rama = Rama.objects.all().first()
        self.rama2 = Rama.objects.filter(name='rama2').first()

        self.ramshik1 = User.objects.get(username='ramshik1')

        self.seller1 = User.objects.get(username='sergei')
        self.seller2 = User.objects.get(username='seller1')
        self.kladman = User.objects.get(username='kladman')

        self.manager1 = User.objects.get(username='manager1')
        self.manager1.account.can_see_rama_cash.add(self.rama)
        self.manager2 = User.objects.get(username='manager2')
        self.manager1.account.can_see_rama_cash.add(self.rama2)

        self.capo1 = User.objects.get(username='capo1')
        self.capo1.account.can_see_rama_cash.add(self.rama, self.rama2)

        self.capo2 = User.objects.get(username='capo2')
        self.capo2.account.can_see_rama_cash.add(self.rama2)

        CashRecord.objects.create_withdraw_employee(employee=self.ramshik1.account, amount=100,
         initiator=self.manager1)

        CashRecord.objects.create_withdraw_cash_from_manager(manager_account=self.manager2.account,
         amount=150, initiator=self.manager2)

    def test_get_rama_cash(self):
        self.client.force_authenticate(user=self.capo1)       
        response = self.client.get(f'/api/common/cash/?rama={self.rama2.pk}')
        self.assertEqual(response.data['count'], 1)
        response = self.client.get(f'/api/common/cash/?rama={self.rama.pk}')
        self.assertEqual(response.data['count'], 1)
        self.client.logout()

    def test_permissions(self):
        self.client.force_authenticate(user=self.capo2)       
        response = self.client.get(f'/api/common/cash/?rama={self.rama.pk}')
        self.assertEqual(response.status_code, 403)
        self.client.logout()


