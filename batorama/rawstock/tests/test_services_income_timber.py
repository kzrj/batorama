# -*- coding: utf-8 -*-
import datetime
from django.test import TestCase, TransactionTestCase
from django.contrib.auth.models import User

from stock.models import Rama
from rawstock.models import Timber, TimberRecord, IncomeTimber

import stock.testing_utils as lumber_testing
import rawstock.testing_utils as timber_testing


class LumberRecordsServisesTest(TransactionTestCase):
    def setUp(self):
        lumber_testing.create_init_data()
        timber_testing.create_test_timber()

        self.seller1 = User.objects.get(username='seller1')
        self.kladman = User.objects.get(username='kladman')

        self.pine_timber20 = Timber.objects.get(diameter=20, wood_species='pine')
        self.pine_timber22 = Timber.objects.get(diameter=22, wood_species='pine')
        self.pine_timber28 = Timber.objects.get(diameter=28, wood_species='pine')

        self.rama = Rama.objects.all().first()

    def test_create_for_income_from_list(self):
        data_list = [
            {'timber': self.pine_timber20, 'quantity': 10 },
            {'timber': self.pine_timber22, 'quantity': 15 },
            {'timber': self.pine_timber28, 'quantity': 20 },
        ]

        income_timber = IncomeTimber.objects.create_income_timber(raw_timber_records=data_list,
            initiator=self.kladman, rama=self.rama)

        self.assertEqual(income_timber.quantity, 45)
        self.assertEqual(income_timber.volume, 9.94)
        self.assertEqual(income_timber.rama, self.rama)
        self.assertEqual(income_timber.initiator, self.kladman)
        self.assertEqual(income_timber.timber_records.all().count(), 3)
