# # -*- coding: utf-8 -*-
from django.contrib.auth.models import User

from stock.models import (Lumber, Shift, LumberRecord, Rama)
from accounts.models import (Account, CashRecord)


def create_test_employee(name, is_ramshik=False, is_senior_ramshik=False, is_manager=False, 
        is_kladman=False, is_seller=False):
    rama = Rama.objects.all().first()
    user = User.objects.create_user(username=name, password='123')
    emp = Account.objects.create(user=user, is_ramshik=is_ramshik, nickname=name, rama=rama,
        is_senior_ramshik=is_senior_ramshik, is_manager=is_manager, is_kladman=is_kladman,
        is_seller=is_seller)
    return user

def create_test_users():
    admin = create_test_employee(name='admin', is_manager=True)
    ramshik1 = create_test_employee(name='ramshik1', is_ramshik=True, is_senior_ramshik=True)
    ramshik2 = create_test_employee(name='ramshik2', is_ramshik=True)
    ramshik3 = create_test_employee(name='ramshik3', is_ramshik=True)
    ramshik4 = create_test_employee(name='ramshik4', is_ramshik=True)
    kladman = create_test_employee(name='kladman', is_kladman=True, is_seller=True)
    seller = create_test_employee(name='seller1', is_seller=True)
    
def create_test_lumber():
    Lumber.objects.create(name='брус 10*15', width=0.1, height=0.15, length=4, volume=0.06,
     employee_rate=600, wood_species='pine', lumber_type='brus', market_cost=12500)
    Lumber.objects.create(name='брус 10*10', width=0.1, height=0.1, length=4, volume=0.04,
     employee_rate=600, wood_species='pine', lumber_type='brus', market_cost=10500)
    Lumber.objects.create(name='брус 10*18', width=0.1, height=0.18, length=4, volume=0.072,
     employee_rate=600, wood_species='pine', lumber_type='brus', market_cost=13500)
    Lumber.objects.create(name='брус 15*18', width=0.15, height=0.18, length=4, volume=0.108,
     employee_rate=600, wood_species='pine', lumber_type='brus', market_cost=14500,
     china_width=0.148, china_height=0.148, china_length=4, china_volume=0.087616)
    Lumber.objects.create(name='брус 18*18', width=0.18, height=0.18, length=4, volume=0.1296,
     employee_rate=600, wood_species='pine', lumber_type='brus', market_cost=15500,
     china_width=0.178, china_height=0.178, china_length=4, china_volume=0.126736)
    
    Lumber.objects.create(name='брус 20*20', width=0.2, height=0.2, length=4, volume=0.16,
     employee_rate=600, wood_species='pine', lumber_type='brus', market_cost=13500)
    Lumber.objects.create(name='брус 20*25', width=0.20, height=0.25, length=4, volume=0.2,
     employee_rate=600, wood_species='pine', lumber_type='brus', market_cost=14500)
    Lumber.objects.create(name='брус 25*25', width=0.25, height=0.25, length=4, volume=0.25,
     employee_rate=600, wood_species='pine', lumber_type='brus', market_cost=15500)
    Lumber.objects.create(name='брус 25*30', width=0.25, height=0.3, length=4, volume=0.3,
     employee_rate=600, wood_species='pine', lumber_type='brus', market_cost=15500)
    Lumber.objects.create(name='брус 30*30', width=0.3, height=0.3, length=4, volume=0.36,
     employee_rate=600, wood_species='pine', lumber_type='brus', market_cost=15500)

    Lumber.objects.create(name='брус 5*5', width=0.05, height=0.05, length=4, volume=0.01,
     employee_rate=600, wood_species='pine', lumber_type='brus', market_cost=15500)

    Lumber.objects.create(name='доска 4*18', width=0.04, height=0.18, length=4, volume=0.0288,
     employee_rate=600, wood_species='pine', lumber_type='doska', market_cost=7500)
    Lumber.objects.create(name='доска 4*15', width=0.04, height=0.15, length=4, volume=0.024,
     employee_rate=600, wood_species='pine', lumber_type='doska', market_cost=7500)
    Lumber.objects.create(name='доска 5*18', width=0.05, height=0.18, length=4, volume=0.036,
     employee_rate=600, wood_species='pine', lumber_type='doska', market_cost=7500)
    Lumber.objects.create(name='доска 5*15', width=0.05, height=0.15, length=4, volume=0.03,
     employee_rate=600, wood_species='pine', lumber_type='doska', market_cost=7500)
    Lumber.objects.create(name='доска 2.5*15', width=0.025, height=0.15, length=4, volume=0.015,
     employee_rate=600, wood_species='pine', lumber_type='doska', market_cost=7500)
    Lumber.objects.create(name='доска 2.5*18', width=0.025, height=0.18, length=4, volume=0.018,
     employee_rate=600, wood_species='pine', lumber_type='doska', market_cost=7500)

    Lumber.objects.create(name='доска 5*10', width=0.05, height=0.1, length=4, volume=0.02,
     employee_rate=800, wood_species='pine', lumber_type='doska', market_cost=7500)
    Lumber.objects.create(name='заборка 2.5*18', width=0.025, height=0.18, length=4, volume=0.018,
     employee_rate=300, wood_species='pine', lumber_type='doska', market_cost=7500)

    Lumber.objects.create(name='брус 10*15', width=0.1, height=0.15, length=4, volume=0.06,
     employee_rate=600, wood_species='larch', lumber_type='brus', market_cost=12500)
    Lumber.objects.create(name='брус 10*10', width=0.1, height=0.1, length=4, volume=0.04,
     employee_rate=600, wood_species='larch', lumber_type='brus', market_cost=12500)
    Lumber.objects.create(name='брус 10*18', width=0.1, height=0.18, length=4, volume=0.072,
     employee_rate=600, wood_species='larch', lumber_type='brus', market_cost=12500)
    Lumber.objects.create(name='брус 15*18', width=0.15, height=0.18, length=4, volume=0.108,
     employee_rate=600, wood_species='larch', lumber_type='brus', market_cost=12500)
    Lumber.objects.create(name='брус 18*18', width=0.18, height=0.18, length=4, volume=0.1296,
     employee_rate=600, wood_species='larch', lumber_type='brus', market_cost=12500)

    Lumber.objects.create(name='доска 4*18', width=0.04, height=0.18, length=4, volume=0.0288,
     employee_rate=600, wood_species='larch', lumber_type='doska', market_cost=7500)
    Lumber.objects.create(name='доска 4*15', width=0.04, height=0.15, length=4, volume=0.024,
     employee_rate=600, wood_species='larch', lumber_type='doska', market_cost=7500)
    Lumber.objects.create(name='доска 5*18', width=0.05, height=0.18, length=4, volume=0.036,
     employee_rate=600, wood_species='larch', lumber_type='doska', market_cost=7500)
    Lumber.objects.create(name='доска 5*15', width=0.05, height=0.15, length=4, volume=0.03,
     employee_rate=600, wood_species='larch', lumber_type='doska', market_cost=7500)
    Lumber.objects.create(name='доска 2.5*15', width=0.025, height=0.15, length=4, volume=0.015,
     employee_rate=600, wood_species='larch', lumber_type='doska', market_cost=7500)
    Lumber.objects.create(name='доска 2.5*18', width=0.025, height=0.18, length=4, volume=0.018,
     employee_rate=600, wood_species='larch', lumber_type='doska', market_cost=7500)

    Lumber.objects.create(name='доска 5*10', width=0.05, height=0.1, length=4, volume=0.02,
     employee_rate=800, wood_species='larch', lumber_type='doska', market_cost=7500)
    Lumber.objects.create(name='заборка 2.5*18', width=0.025, height=0.18, length=4, volume=0.018,
     employee_rate=300, wood_species='larch', lumber_type='doska', market_cost=7500)

def create_test_data():
    create_test_users()
    create_test_lumber()

def create_init_data():
    rama1 = Rama.objects.create(name='batorama')
    create_test_lumber()
    admin = User.objects.create_user(username='bato', password='banzai123')
    Account.objects.create(user=admin, is_manager=True, rama=rama1, nickname='bato')
    
    superuser = User.objects.create_superuser(username='kaizerj', password='batorama123')
    Account.objects.create(user=superuser, is_manager=True, rama=rama1, nickname='kzr')
    create_test_users()
