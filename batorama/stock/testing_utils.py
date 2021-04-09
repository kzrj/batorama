# # -*- coding: utf-8 -*-
from django.contrib.auth.models import User

from stock.models import (Employee, Lumber, Shift, LumberRecord, CashRecord)


def create_test_employee(name):
    user = User.objects.create_user(username=name, password='123')
    emp = Employee.objects.create(user=user)
    return user

def create_test_users():
	admin = create_test_employee('admin')
	ramshik1 = create_test_employee('ramshik1')
	ramshik2 = create_test_employee('ramshik2')
	ramshik3 = create_test_employee('ramshik3')
	ramshik4 = create_test_employee('ramshik4')
	
def create_test_lumber():
	Lumber.objects.create(name='брус 10*15', width=0.1, height=0.15, length=4, volume=0.06)
	Lumber.objects.create(name='брус 10*10', width=0.1, height=0.1, length=4, volume=0.04)
	Lumber.objects.create(name='брус 10*18', width=0.1, height=0.18, length=4, volume=0.072)
	Lumber.objects.create(name='брус 15*18', width=0.15, height=0.18, length=4, volume=0.108)
	Lumber.objects.create(name='брус 18*18', width=0.18, height=0.18, length=4, volume=0.1296)

	Lumber.objects.create(name='доска 4*18', width=0.04, height=0.18, length=4, volume=0.0288)
	Lumber.objects.create(name='доска 4*15', width=0.04, height=0.15, length=4, volume=0.024)
	Lumber.objects.create(name='доска 5*18', width=0.05, height=0.18, length=4, volume=0.036)
	Lumber.objects.create(name='доска 5*15', width=0.05, height=0.15, length=4, volume=0.03)
	Lumber.objects.create(name='доска 2.5*15', width=0.025, height=0.15, length=4, volume=0.015)
	Lumber.objects.create(name='доска 2.5*18', width=0.025, height=0.18, length=4, volume=0.018)

	Lumber.objects.create(name='доска 5*10', width=0.05, height=0.1, length=4, volume=0.02)
	Lumber.objects.create(name='заборка 2.5*18', width=0.025, height=0.18, length=4, volume=0.018)

def create_test_data():
	create_test_users()
	create_test_lumber()


def create_init_data():
	create_test_lumber()
	admin = User.objects.create_user(username='bato', password='banzai123')
	Employee.objects.create(user=admin)
	
	superuser = User.objects.create_superuser(username='kaizerj', password='batorama123')
	Employee.objects.create(user=superuser)
	create_test_users()
	create_test_lumber()
