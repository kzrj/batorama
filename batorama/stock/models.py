# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Q, Subquery, OuterRef, Count, Prefetch, F, Sum, ExpressionWrapper
from django.db.models.functions import Coalesce
from django.contrib.auth.models import User
from django.utils import timezone

from core.models import CoreModel, CoreModelManager


class LumberQuerySet(models.QuerySet):
    # Servises

    # Selectors
    def add_rama_income(self, rama):
        subquery = LumberRecord.objects.calc_total_income_volume_by_rama_by_lumber(
            lumber=OuterRef('pk'), rama=rama)

        return self.annotate(total_income_volume=Coalesce(Subquery(subquery), 0.0))

    def add_rama_outcome(self, rama):
        subquery = LumberRecord.objects.calc_total_outcome_volume_by_rama_by_lumber(
            lumber=OuterRef('pk'), rama=rama)            
        return self.annotate(total_outcome_volume=Coalesce(Subquery(subquery), 0.0))

    def add_rama_income_quantity(self, rama):
        subquery = LumberRecord.objects.calc_total_income_quantity_by_rama_by_lumber(
            lumber=OuterRef('pk'), rama=rama)

        return self.annotate(total_income_quantity=Coalesce(Subquery(subquery), 0))

    def add_rama_outcome_quantity(self, rama):
        subquery = LumberRecord.objects.calc_total_outcome_quantity_by_rama_by_lumber(
            lumber=OuterRef('pk'), rama=rama)            
        return self.annotate(total_outcome_quantity=Coalesce(Subquery(subquery), 0))

    def add_rama_current_stock(self, rama):
        return self.add_rama_income(rama=rama) \
                .add_rama_outcome(rama=rama) \
                .annotate(current_stock_volume=F('total_income_volume') - F('total_outcome_volume')) \
                .add_rama_income_quantity(rama=rama) \
                .add_rama_outcome_quantity(rama=rama) \
                .annotate(current_stock_quantity=F('total_income_quantity') - F('total_outcome_quantity'))


class Lumber(CoreModel):
    name = models.CharField(max_length=100)
    width = models.FloatField()
    length = models.FloatField()
    height = models.FloatField()
    volume = models.FloatField()
    employee_rate = models.IntegerField(default=0)
    market_cost = models.IntegerField(default=0)

    china_width = models.FloatField(null=True, blank=True)
    china_length = models.FloatField(null=True, blank=True)
    china_height = models.FloatField(null=True, blank=True)
    china_volume = models.FloatField(null=True, blank=True)

    round_volume = models.FloatField(default=0)

    SPECIES = [('pine', 'Сосна'), ('larch', 'Лиственница')]
    wood_species = models.CharField(max_length=20, choices=SPECIES)

    LUMBER_TYPES = [('brus', 'brus'), ('doska', 'doska')]
    lumber_type = models.CharField(max_length=20, choices=LUMBER_TYPES)

    objects = LumberQuerySet.as_manager()

    class Meta:
        ordering = ['lumber_type', 'wood_species']

    def __str__(self):
        return f'{self.name} {self.length}'

    @property
    def stock_total_cash(self):
        return self.current_stock_volume * self.market_cost

    @property
    def qnty_in_cube(self):
        return round(1 / self.volume, 3)

    @property
    def china_name(self):
        return f'брус Китай {self.china_width}*{self.china_height}'


class RamaQuerySet(models.QuerySet):
    pass


class Rama(CoreModel):
    name = models.CharField(max_length=50)

    STOCK_TYPES = [('mixed', 'Смешанный'), ('sorted', 'Сортированный')]
    stock_type = models.CharField(max_length=50, choices=STOCK_TYPES, null=True, blank=True)

    SALE_TYPES = [('seller_kladman_split', 'Комиссия продавца и кладмэна раздельно'),
         ('seller_kladman_same', 'Комиссия продавца и кладмэна вместе')]
    sale_type = models.CharField(max_length=100, choices=SALE_TYPES, null=True, blank=True)

    def __str__(self):
        return self.name    


class ShiftQuerySet(models.QuerySet):
    # Servises
    def create_shift(self, shift_type, cash, employees, lumber_records, initiator=None,
         date=None, note=None):
        if not date:
            date = timezone.now()
        shift = self.create(shift_type=shift_type, date=date, employee_cash=cash, 
            initiator=initiator, rama=initiator.account.rama, note=note)
        shift.employees.add(*employees)
        lumber_records.update(shift=shift)
        shift.back_calc_volume = lumber_records.calc_total_volume()
        shift.volume = shift.back_calc_volume
        shift.back_calc_cash = lumber_records.calc_total_cash()
        shift.back_calc_cash_per_employee = shift.back_calc_cash / len(employees)
        shift.cash_per_employee = shift.employee_cash / len(employees)
        shift.save()

        for emp in employees:
            emp.cash_records.create_payout_from_shift(employee=emp, shift=shift,
             amount=shift.cash_per_employee, initiator=initiator,
              note=f'Начисление рамщику {emp.nickname} за смену #{shift.pk}')

        return shift

    def create_shift_raw_records(self, **kwargs):
        lumber_records = LumberRecord.objects.create_from_list(records_list=kwargs['raw_records'],
            rama=kwargs['rama'])
        kwargs['lumber_records'] = LumberRecord.objects.filter(pk__in=(lr.pk for lr in lumber_records))
        del kwargs['raw_records']
        del kwargs['rama']
        return self.create_shift(**kwargs)

    # Selectors


class Shift(CoreModel):
    date = models.DateTimeField(null=True, blank=True)
    rama = models.ForeignKey(Rama, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='shifts')

    SHIFT_TYPES = [('day', 'День'), ('night', 'Ночь')]
    shift_type = models.CharField(max_length=10, choices=SHIFT_TYPES)

    employees = models.ManyToManyField('accounts.Account')
    initiator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='shifts')

    volume = models.FloatField(null=True)

    employee_cash = models.FloatField(null=True)
    cash_per_employee = models.FloatField(null=True)

    back_calc_volume = models.FloatField(null=True)
    back_calc_cash = models.FloatField(null=True)
    back_calc_cash_per_employee = models.FloatField(null=True)

    note = models.TextField(null=True, blank=True)

    objects = ShiftQuerySet.as_manager()

    class Meta:
        ordering = ['date',]

    def __str__(self):
        return f'Cмена {self.shift_type} {self.date.strftime("%d-%m-%Y")}'

    @property
    def get_empoyees(self):
        return self.employees.all()

    @property
    def volume_without_zabor(self):
        zabor_volume = self.lumber_records.filter(lumber__name__contains='забор') \
                                          .aggregate(zabor=Coalesce(Sum('volume'), 0.0))['zabor']
        return self.volume - zabor_volume


class SaleQuerySet(models.QuerySet):
    # Servises
    def create_sale_common(self, raw_records, initiator, seller=None, bonus_kladman=None,
        loader=False, delivery_fee=0, add_expenses=0, note=None, date=None, client=None):
        if not date:
            date = timezone.now()

        sale = self.create(date=date, initiator=initiator, delivery_fee=delivery_fee,
            seller=seller, bonus_kladman=bonus_kladman,
            rama=initiator.account.rama, add_expenses=add_expenses, note=note, client=client)

        lumber_records = LumberRecord.objects.create_from_raw_for_common_sale(
            records_list=raw_records, rama=initiator.account.rama)
        lumber_records = LumberRecord.objects.filter(pk__in=(lr.pk for lr in lumber_records))
        lumber_records.update(sale=sale)

        volume_and_cash = lumber_records.calc_sale_volume_and_cash()
        sale.volume = volume_and_cash['total_volume']
        sale.rama_total_cash = round(volume_and_cash['rama_cash'])
        sale.selling_total_cash = round(volume_and_cash['sale_cash'])

        sale.cash_records.create_income_from_sale(amount=sale.selling_total_cash,
            note=f'приход с продажи {sale.client}', initiator=initiator, sale=sale)

        sale.calc_seller_fee()
        sale.calc_kladman_fee()
        if loader: 
            sale.calc_loader_fee()

        sale.save()
        return sale

    # Selectors
    def calc_totals(self):
        return self.aggregate(
            total_volume=Sum('volume'),
            total_selling_cash=Sum('selling_total_cash'),
            total_rama_cash=Sum('rama_total_cash'),
            total_seller_fee=Sum('seller_fee'),
            total_loader_fee=Sum('loader_fee'),
            total_kladman_fee=Sum('kladman_fee'),
            total_delivery_fee=Sum('delivery_fee'),
            total_add_expenses=Sum('add_expenses'),
            )

    def add_only_brus_volume(self, wood_species='pine'):
        subquery = LumberRecord.objects.filter(sale__pk=OuterRef('pk'), lumber__wood_species=wood_species) \
                            .filter(Q(lumber__lumber_type='brus') | Q(lumber__name__contains='обрезная')) \
                            .exclude(lumber__width=0.025) \
                        .values('sale') \
                        .annotate(brus_volume=Sum('volume')) \
                        .values('brus_volume')

        return self.annotate(brus_volume=Coalesce(Subquery(subquery), 0.0))

    def add_only_doska_volume_exclude_2_5(self, wood_species='pine'):
        subquery = LumberRecord.objects.filter(sale__pk=OuterRef('pk'),
                            lumber__lumber_type='doska', lumber__wood_species=wood_species) \
                        .exclude(lumber__width=0.025) \
                        .exclude(lumber__name__contains='обрезная') \
                        .values('sale') \
                        .annotate(doska_volume=Sum('volume')) \
                        .values('doska_volume')

        return self.annotate(doska_volume=Coalesce(Subquery(subquery), 0.0))

    def calc_sold_volume_for_quota_calc(self, wood_species='pine'):
        return self.add_only_brus_volume(wood_species=wood_species) \
                   .add_only_doska_volume_exclude_2_5(wood_species=wood_species) \
                   .aggregate(total_brus_volume=Coalesce(Sum('brus_volume'), 0.0),
                              total_doska_volume=Coalesce(Sum('doska_volume'), 0.0))


class Sale(CoreModel):
    date = models.DateTimeField(null=True, blank=True)
    rama = models.ForeignKey(Rama, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='sales')

    SALE_TYPES = [('person', 'Физ. лицо'), ('perekup', 'Перекуп'), ('china', 'Китай')]
    sale_type = models.CharField(max_length=20, choices=SALE_TYPES, null=True, blank=True)

    client = models.CharField(max_length=20, null=True, blank=True)

    initiator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
        related_name='sales')
    volume = models.FloatField(null=True, blank=True)

    note = models.TextField(null=True, blank=True)

    rama_total_cash = models.IntegerField(default=0)
    selling_total_cash = models.IntegerField(default=0)

    seller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
        related_name='sales_as_seller')
    bonus_kladman = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
        related_name='sales_as_bonus_kladman')

    seller_fee = models.IntegerField(default=0, null=True, blank=True)
    kladman_fee = models.IntegerField(default=0,null=True, blank=True)
    loader_fee = models.IntegerField(default=0, null=True, blank=True)
    delivery_fee = models.IntegerField(default=0, null=True, blank=True)

    system_fee = models.IntegerField(default=0, null=True, blank=True)

    add_expenses = models.IntegerField(default=0, null=True, blank=True)

    objects = SaleQuerySet.as_manager()

    def calc_seller_fee(self):
        if self.seller:
            self.seller_fee = round(self.selling_total_cash - self.rama_total_cash)
            # self.cash_records.create_rama_expense(
            #     amount=self.seller_fee, note=f'Вознаграждение продавца с продажи {self.client}',
            #     initiator=self.initiator, rama=self.rama)

    def calc_kladman_fee(self):
        if self.bonus_kladman:
            self.kladman_fee = self.system_fee = round(self.volume * 100)
            # self.cash_records.create_rama_expense(
            #     amount=self.kladman_fee, note=f'Вознаграждение кладмэна с продажи {self.client}',
            #     initiator=self.initiator, rama=self.rama)

    def calc_loader_fee(self):
        self.loader_fee = round(self.volume * 100)
        # self.cash_records.create_rama_expense(
        #         amount=self.loader_fee, note=f'Вознаграждение грузчика с продажи {self.client}',
        #         initiator=self.initiator, rama=self.rama)

    @property
    def seller_name(self):
        if self.seller:
            return self.seller.account.nickname
        return None
 

class LumberRecordQuerySet(models.QuerySet):
    # Servises
    def create_from_list(self, records_list, rama=None):
        lumber_records = list()
        for record in records_list:
            if record['quantity'] > 0:
                rate = record.get('rate') or record.get('employee_rate')
                lumber_records.append(
                    LumberRecord(
                        lumber=record['lumber'],
                        quantity=record['quantity'],
                        volume=record['quantity']*record['lumber'].volume, 
                        rate=rate,
                        total_cash=record['cash'], 
                        back_total_cash=rate*record['quantity']*record['lumber'].volume,
                        rama=rama)
                )
        return self.bulk_create(lumber_records)

    def create_from_raw_for_common_sale(self, records_list, rama=None):
        lumber_records = list()
        for record in records_list:
            if record['quantity'] > 0:
                selling_calc_type = record.get('calc_type', None)
                rama_total_cash = record['rama_price']*record['quantity']*record['lumber'].volume
                if selling_calc_type == 'china':
                    rama_total_cash = record['rama_price']*record['quantity']*record['lumber'].china_volume                   

                lumber_records.append(
                    LumberRecord(
                        lumber=record['lumber'],
                        quantity=record['quantity'],
                        volume=record['quantity']*record['lumber'].volume,

                        rama_price=record['rama_price'],
                        rama_total_cash=rama_total_cash,

                        selling_price=record['selling_price'],
                        selling_total_cash=record['selling_total_cash'],

                        selling_calc_type=selling_calc_type,
                        rama=rama
                    )
                )
        return self.bulk_create(lumber_records)

    def create_for_resaw(self, lumber, quantity, rama):
        return self.create(lumber=lumber, quantity=quantity, rama=rama, record_type='resaw_record',
            volume=lumber.volume * quantity)

    def create_for_refuse(self, lumber, quantity, rama):
        return self.create(lumber=lumber, quantity=quantity, rama=rama, record_type='refuse_record',
            volume=lumber.volume * quantity)

    # Selectors
    def calc_total_volume(self):
        return self.aggregate(total_volume=Sum('volume'))['total_volume']

    def calc_total_cash(self):
        return self.aggregate(cash=Sum('total_cash'))['cash']

    def calc_total_income_volume_by_rama_by_lumber(self, lumber, rama):
        return self.filter(lumber=lumber, rama=rama) \
            .filter(Q(shift__isnull=False) | Q(re_saw_out__isnull=False)) \
            .values('rama') \
            .annotate(total_income_volume=Sum('volume')) \
            .values('total_income_volume')

    def calc_total_outcome_volume_by_rama_by_lumber(self, lumber, rama):
        return self.filter(lumber=lumber, rama=rama) \
            .filter(Q(sale__isnull=False) | Q(re_saw_in__isnull=False) | Q(refuse__isnull=False)) \
            .values('rama') \
            .annotate(total_outcome_volume=Sum('volume')) \
            .values('total_outcome_volume')

    def calc_total_income_quantity_by_rama_by_lumber(self, lumber, rama):
        return self.filter(lumber=lumber, rama=rama) \
            .filter(Q(shift__isnull=False) | Q(re_saw_out__isnull=False)) \
            .values('rama') \
            .annotate(total_income_quantity=Sum('quantity')) \
            .values('total_income_quantity')

    def calc_total_outcome_quantity_by_rama_by_lumber(self, lumber, rama):
        return self.filter(lumber=lumber, rama=rama) \
            .filter(Q(sale__isnull=False) | Q(re_saw_in__isnull=False) | Q(refuse__isnull=False)) \
            .values('rama') \
            .annotate(total_outcome_quantity=Sum('quantity')) \
            .values('total_outcome_quantity')

    def calc_rama_total_cash(self):
        return self.aggregate(cash=Sum('rama_total_cash'))['cash']

    def calc_selling_total_cash(self):
        return self.aggregate(cash=Sum('selling_total_cash'))['cash']

    def calc_rama_and_selling_total_cash(self):
        return self.aggregate(rama_cash=Sum('rama_total_cash'), sale_cash=Sum('selling_total_cash'))

    def calc_sale_volume_and_cash(self):
        return self.aggregate(
            rama_cash=Sum('rama_total_cash'),
            sale_cash=Sum('selling_total_cash'),
            total_volume=Sum('volume'))

    # def calc_brus_and_doska_volume(self):
    #     return self.aggregate(
    #         rama_cash=Sum('rama_total_cash', filter=()),
    #         sale_cash=Sum('selling_total_cash'),
    #         total_volume=Sum('volume'))


class LumberRecord(CoreModel):
    RECORD_TYPES = [('shift_record', 'shift_record'), ('sale_record', 'sale_record'),
     ('resaw_record', 'resaw_record'), ('refuse_record', 'refuse_record')]
    record_type = models.CharField(max_length=50, choices=RECORD_TYPES, null=True, blank=True)

    lumber = models.ForeignKey(Lumber, on_delete=models.CASCADE, related_name='records')
    rama = models.ForeignKey(Rama, on_delete=models.SET_NULL, null=True, blank=True, 
        related_name='lumber_records')
    quantity = models.IntegerField(default=0)
    volume = models.FloatField(default=0)
    rate = models.IntegerField(default=0)

    total_cash = models.FloatField(default=0)
    back_total_cash = models.FloatField(default=0)

    rama_price = models.IntegerField(default=0)
    rama_total_cash = models.FloatField(default=0)

    selling_price = models.IntegerField(default=0)
    selling_total_cash = models.FloatField(default=0)

    selling_calc_type = models.CharField(max_length=10, null=True, blank=True)

    shift = models.ForeignKey(Shift, on_delete=models.CASCADE, null=True, related_name='lumber_records')

    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, null=True, related_name='lumber_records')

    objects = LumberRecordQuerySet.as_manager()

    class Meta:
        ordering = ['lumber__wood_species', 'lumber__lumber_type']

    def __str__(self):
        return f'{self.lumber} {self.quantity}'


class ReSawQuerySet(models.QuerySet):
    def create_resaw(self, resaw_lumber_in, resaw_lumber_out, rama, employees=None, employee_cash=None,
        initiator=None):
        lumber_in = LumberRecord.objects.create_for_resaw(
            lumber=resaw_lumber_in['lumber'], quantity=resaw_lumber_in['quantity'], rama=rama)
        lumber_out = LumberRecord.objects.create_for_resaw(
            lumber=resaw_lumber_out['lumber'], quantity=resaw_lumber_out['quantity'], rama=rama)
        resaw = self.create(lumber_in=lumber_in, lumber_out=lumber_out, employee_cash=employee_cash,
            initiator=initiator, rama=rama)
        # add employees, employee_cash

        return resaw
        

class ReSaw(CoreModel):
    rama = models.ForeignKey(Rama, on_delete=models.SET_NULL, null=True, blank=True, 
        related_name='resaws')
    employee_cash = models.IntegerField(null=True, blank=True)
    employees = models.ManyToManyField('accounts.Account')
    lumber_in = models.OneToOneField(LumberRecord, on_delete=models.CASCADE, related_name='re_saw_in')
    lumber_out = models.OneToOneField(LumberRecord, on_delete=models.CASCADE, related_name='re_saw_out')

    initiator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
        related_name='resaws')

    objects = ReSawQuerySet.as_manager()


    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Перепил {self.pk}'


class RefuseLumberQuerySet(models.QuerySet):
    def create_refuse(self, lumber, quantity, rama, initiator=None):
        lumber = LumberRecord.objects.create_for_refuse(
            lumber=lumber, quantity=quantity, rama=rama)
        
        resaw = self.create(lumber=lumber, initiator=initiator)

        return resaw
        

class RefuseLumber(CoreModel):
    lumber = models.OneToOneField(LumberRecord, on_delete=models.CASCADE, related_name='refuse')

    initiator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
        related_name='refuses')

    objects = RefuseLumberQuerySet.as_manager()

    def __str__(self):
        return f'Брак {self.pk}'


class LumberSawRate(CoreModel):
    lumber = models.ForeignKey(Lumber, on_delete=models.CASCADE, related_name='saw_rates')
    rama = models.ForeignKey(Rama, on_delete=models.CASCADE, related_name='saw_rates')
    employee_rate = models.IntegerField()

    def __str__(self):
        return f'Ставка рамщика {self.pk}'