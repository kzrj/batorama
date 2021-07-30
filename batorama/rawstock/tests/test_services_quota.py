# -*- coding: utf-8 -*-
import datetime
from django.test import TestCase, TransactionTestCase
from django.contrib.auth.models import User

from stock.models import Rama
from rawstock.models import Timber, TimberRecord, IncomeTimber, Quota

import stock.testing_utils as lumber_testing
import rawstock.testing_utils as timber_testing


class OuotaServisesTest(TransactionTestCase):
    def setUp(self):
        lumber_testing.create_init_data()
        timber_testing.create_test_timber()

        self.seller1 = User.objects.get(username='seller1')
        self.kladman = User.objects.get(username='kladman')

        self.pine_timber20 = Timber.objects.get(diameter=20, wood_species='pine')
        self.pine_timber22 = Timber.objects.get(diameter=22, wood_species='pine')
        self.pine_timber28 = Timber.objects.get(diameter=28, wood_species='pine')

        self.larch_timber20 = Timber.objects.get(diameter=20, wood_species='larch')
        self.larch_timber22 = Timber.objects.get(diameter=22, wood_species='larch')
        self.larch_timber28 = Timber.objects.get(diameter=28, wood_species='larch')

        self.rama = Rama.objects.all().first()

        data_list = [
            {'timber': self.pine_timber20, 'quantity': 10 },
            {'timber': self.pine_timber22, 'quantity': 15 },
            {'timber': self.pine_timber28, 'quantity': 20 },
            {'timber': self.larch_timber20, 'quantity': 11 },
            {'timber': self.larch_timber22, 'quantity': 22 },
            {'timber': self.larch_timber28, 'quantity': 33 },
        ]

        self.income_timber = IncomeTimber.objects.create_income_timber(raw_timber_records=data_list,
            initiator=self.kladman, rama=self.rama)

    def test_create_quota(self):
        quotas = Quota.objects.create_quota(income_timber=self.income_timber)

        self.assertEqual(quotas['pine_quota'].volume_quota_brus, 4.97)
        self.assertEqual(quotas['pine_quota'].volume_quota_doska, 1.988)
        self.assertEqual(quotas['pine_quota'].rama, self.rama)
        self.assertEqual(quotas['pine_quota'].wood_species, 'pine')