# # -*- coding: utf-8 -*-
from django.contrib.auth.models import User

from rawstock.models import (Timber, TimberRecord)

   
def create_test_timber():
    Timber.objects.create(length=4, volume=0.053, wood_species='pine', diameter=12)
    Timber.objects.create(length=4, volume=0.073, wood_species='pine', diameter=14)
    Timber.objects.create(length=4, volume=0.095, wood_species='pine', diameter=16)
    Timber.objects.create(length=4, volume=0.12,  wood_species='pine', diameter=18)
    Timber.objects.create(length=4, volume=0.147, wood_species='pine', diameter=20)
    Timber.objects.create(length=4, volume=0.178, wood_species='pine', diameter=22)
    Timber.objects.create(length=4, volume=0.21,  wood_species='pine', diameter=24)
    Timber.objects.create(length=4, volume=0.25,  wood_species='pine', diameter=26)
    Timber.objects.create(length=4, volume=0.29,  wood_species='pine', diameter=28)
    Timber.objects.create(length=4, volume=0.33,  wood_species='pine', diameter=30)
    Timber.objects.create(length=4, volume=0.38,  wood_species='pine', diameter=32)
    Timber.objects.create(length=4, volume=0.43,  wood_species='pine', diameter=34)
    Timber.objects.create(length=4, volume=0.48,  wood_species='pine', diameter=36)
    Timber.objects.create(length=4, volume=0.53,  wood_species='pine', diameter=38)
    Timber.objects.create(length=4, volume=0.58,  wood_species='pine', diameter=40)

    Timber.objects.create(length=4, volume=0.053, wood_species='larch', diameter=12)
    Timber.objects.create(length=4, volume=0.073, wood_species='larch', diameter=14)
    Timber.objects.create(length=4, volume=0.095, wood_species='larch', diameter=16)
    Timber.objects.create(length=4, volume=0.12,  wood_species='larch', diameter=18)
    Timber.objects.create(length=4, volume=0.147, wood_species='larch', diameter=20)
    Timber.objects.create(length=4, volume=0.178, wood_species='larch', diameter=22)
    Timber.objects.create(length=4, volume=0.21,  wood_species='larch', diameter=24)
    Timber.objects.create(length=4, volume=0.25,  wood_species='larch', diameter=26)
    Timber.objects.create(length=4, volume=0.29,  wood_species='larch', diameter=28)
    Timber.objects.create(length=4, volume=0.33,  wood_species='larch', diameter=30)
    Timber.objects.create(length=4, volume=0.38,  wood_species='larch', diameter=32)
    Timber.objects.create(length=4, volume=0.43,  wood_species='larch', diameter=34)
    Timber.objects.create(length=4, volume=0.48,  wood_species='larch', diameter=36)
    Timber.objects.create(length=4, volume=0.53,  wood_species='larch', diameter=38)
    Timber.objects.create(length=4, volume=0.58,  wood_species='larch', diameter=40)

    