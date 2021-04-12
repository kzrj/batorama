# # -*- coding: utf-8 -*-
from django.contrib.auth.models import User

from stock.models import (Employee, Lumber, Shift, LumberRecord, CashRecord)


def create_test_employee(name, is_ramshik1=False, is_senior_ramshik=False, is_manager=False):
    user = User.objects.create_user(username=name, password='123')
    emp = Employee.objects.create(user=user)
    return user

def create_test_users():
    admin = create_test_employee(name='admin', is_manager=True)
    ramshik1 = create_test_employee(name='ramshik1', is_ramshik=True, is_senior_ramshik=True)
    ramshik2 = create_test_employee(name='ramshik2', is_ramshik=True)
    ramshik3 = create_test_employee(name='ramshik3', is_ramshik=True)
    ramshik4 = create_test_employee(name='ramshik4', is_ramshik=True)
    
def create_test_lumber():
    Lumber.objects.create(name='брус 10*15', width=0.1, height=0.15, length=4, volume=0.06, employee_rate=600)
    Lumber.objects.create(name='брус 10*10', width=0.1, height=0.1, length=4, volume=0.04, employee_rate=600)
    Lumber.objects.create(name='брус 10*18', width=0.1, height=0.18, length=4, volume=0.072, employee_rate=600)
    Lumber.objects.create(name='брус 15*18', width=0.15, height=0.18, length=4, volume=0.108, employee_rate=600)
    Lumber.objects.create(name='брус 18*18', width=0.18, height=0.18, length=4, volume=0.1296, employee_rate=600)

    Lumber.objects.create(name='доска 4*18', width=0.04, height=0.18, length=4, volume=0.0288, employee_rate=600)
    Lumber.objects.create(name='доска 4*15', width=0.04, height=0.15, length=4, volume=0.024, employee_rate=600)
    Lumber.objects.create(name='доска 5*18', width=0.05, height=0.18, length=4, volume=0.036, employee_rate=600)
    Lumber.objects.create(name='доска 5*15', width=0.05, height=0.15, length=4, volume=0.03, employee_rate=600)
    Lumber.objects.create(name='доска 2.5*15', width=0.025, height=0.15, length=4, volume=0.015, employee_rate=600)
    Lumber.objects.create(name='доска 2.5*18', width=0.025, height=0.18, length=4, volume=0.018, employee_rate=600)

    Lumber.objects.create(name='доска 5*10', width=0.05, height=0.1, length=4, volume=0.02, employee_rate=800)
    Lumber.objects.create(name='заборка 2.5*18', width=0.025, height=0.18, length=4, volume=0.018, employee_rate=300)

def create_test_data():
    create_test_users()
    create_test_lumber()


def create_init_data():
    create_test_lumber()
    admin = User.objects.create_user(username='bato', password='banzai123')
    Employee.objects.create(user=admin, is_manager=True)
    
    superuser = User.objects.create_superuser(username='kaizerj', password='batorama123')
    Employee.objects.create(user=superuser)
    create_test_users()
    create_test_lumber()
