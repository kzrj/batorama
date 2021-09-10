# # -*- coding: utf-8 -*-
import time

from django.contrib.auth.models import User
from django.db.models import Q, Subquery, OuterRef, Count, Prefetch, F, Sum

from rest_framework.response import Response
from rest_framework import generics, serializers, permissions, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from django_filters import rest_framework as filters

from stock.models import Lumber, Rama, LumberRecord, Shift, Sale, ReSaw
from cash.models import CashRecord 
from rawstock.models import TimberRecord, IncomeTimber, Timber, Quota

from core.serializers import AnnotateFieldsModelSerializer, ChoiceField


# rama stock
class LumberStockListView(generics.ListAPIView):

    class LumberStockReadSerializer(AnnotateFieldsModelSerializer):
        stock_total_cash = serializers.ReadOnlyField()
        
        class Meta:
            model = Lumber
            fields = '__all__'


    class LumberStockFilter(filters.FilterSet):
        rama = filters.NumberFilter(method='filter_rama')

        def filter_rama(self, queryset, name, value):
            rama = Rama.objects.filter(pk=value).first()
            if rama:
                return queryset.add_rama_current_stock(rama=rama)
            return queryset

        class Meta:
            model = Lumber
            fields = '__all__'


    class CanSeeRamaStockPermissions(permissions.BasePermission):
        def has_permission(self, request, view):
            if request.method in permissions.SAFE_METHODS:
                if request.GET.get('rama') and \
                    (int(request.GET.get('rama'))
                        in request.user.account.can_see_rama_stock.all().values_list('pk', flat=True)):
                    return True
            return False

    queryset = Lumber.objects.all().prefetch_related('records')
    serializer_class = LumberStockReadSerializer
    permission_classes = [IsAuthenticated, CanSeeRamaStockPermissions]
    filter_class = LumberStockFilter


# shifts list
class ShiftListView(generics.ListAPIView):

    class ShiftReadSerializer(serializers.ModelSerializer):

        class LumberRecordSerializer(serializers.ModelSerializer):
            lumber = serializers.StringRelatedField()
            wood_species = serializers.ReadOnlyField(source='lumber.wood_species')

            class Meta:
                model = LumberRecord
                fields = ('lumber', 'quantity', 'volume', 'rate', 'total_cash', 'back_total_cash',
                 'wood_species',)

        lumber_records = LumberRecordSerializer(many=True)
        employees = serializers.StringRelatedField(read_only=True, many=True)
        date = serializers.DateTimeField(format='%d/%m', read_only=True)
        volume_without_zabor = serializers.ReadOnlyField()

        class Meta:
            model = Shift
            fields = '__all__'


    class ShiftFilter(filters.FilterSet):
        date = filters.DateFromToRangeFilter()

        class Meta:
            model = Shift
            fields = ['rama', 'date']


    class CanSeeRamaShiftPermissions(permissions.BasePermission):
        def has_permission(self, request, view):
            if request.method in permissions.SAFE_METHODS:
                if request.GET.get('rama') and \
                    (int(request.GET.get('rama'))
                        in request.user.account.can_see_rama_shift.all().values_list('pk', flat=True)):
                    return True
            return False

    queryset = Shift.objects.all().prefetch_related('lumber_records')
    serializer_class = ShiftReadSerializer
    permission_classes = [IsAuthenticated, CanSeeRamaShiftPermissions ]
    filter_class = ShiftFilter


# sales list
class SalesListView(generics.ListAPIView):

    class SaleReadSerializer(serializers.ModelSerializer):

        class SaleLumberRecordSerializer(serializers.ModelSerializer):
            lumber = serializers.StringRelatedField()
            wood_species = ChoiceField(source='lumber.wood_species', read_only=True,
             choices=Lumber.SPECIES)
            
            class Meta:
                model = LumberRecord
                fields = ['lumber', 'quantity', 'volume', 'selling_price', 'selling_total_cash',
                 'rama_price', 'rama_total_cash', 'wood_species']

        lumber_records = SaleLumberRecordSerializer(many=True)
        initiator = serializers.ReadOnlyField(source='initiator.account.nickname')
        seller_name = serializers.ReadOnlyField()
        date = serializers.DateTimeField(format='%d/%m', read_only=True)

        class Meta:
            model = Sale
            exclude = ['created_at', 'modified_at']


    class SaleFilter(filters.FilterSet):
        date = filters.DateFromToRangeFilter()

        class Meta:
            model = Sale
            fields = ['rama', 'date', 'seller']


    class CanSeeRamaSalePermissions(permissions.BasePermission):
        def has_permission(self, request, view):
            if request.method in permissions.SAFE_METHODS:
                acc = request.user.account
                rama = request.GET.get('rama')
                can_see_ramas_list = acc.can_see_rama_sales.all().values_list('pk', flat=True)

                if rama:
                    if acc.is_boss or request.user.is_staff:
                        return True

                    if acc.is_manager and acc.rama.pk == int(rama):
                        return True

                    if acc.is_seller and request.GET.get('seller') \
                      and int(rama) in can_see_ramas_list:
                        return True

                    if acc.is_capo and int(rama) in can_see_ramas_list:
                        return True
            return False

    queryset = Sale.objects.all() \
        .select_related('initiator__account') \
        .prefetch_related('lumber_records__lumber',)
    serializer_class = SaleReadSerializer
    permission_classes = [IsAuthenticated, CanSeeRamaSalePermissions ]
    filter_class = SaleFilter

    def list(self, request):
        data = dict()
        queryset = self.filter_queryset(self.get_queryset())
                
        serializer = self.SaleReadSerializer(queryset, many=True)
        data['sales'] = serializer.data
        data['totals'] = queryset.calc_totals()

        return Response(data)


# cashrecords list
class CashRecordsListView(generics.ListAPIView):

    class CashRecordSerializer(serializers.ModelSerializer):
        class Meta:
            model = CashRecord
            fields = ['created_at', 'amount', 'note', 'record_type']


    class ExpensesFilter(filters.FilterSet):
        created_at = filters.DateFromToRangeFilter()

        class Meta:
            model = CashRecord
            fields = ['created_at', 'rama']


    class CanSeeRamaCashPermissions(permissions.BasePermission):
        def has_permission(self, request, view):
            if request.method in permissions.SAFE_METHODS:
                acc = request.user.account
                rama = request.GET.get('rama')
                can_see_ramas_list = acc.can_see_rama_cash.all().values_list('pk', flat=True)

                if rama and (int(rama)) in can_see_ramas_list:
                    return True
            return False

    queryset = CashRecord.objects.all()
    serializer_class = CashRecordSerializer
    permission_classes = [IsAuthenticated, CanSeeRamaCashPermissions]
    filter_class = ExpensesFilter


# daily reports
class DailyReport(APIView):

    class DateSerializer(serializers.Serializer):
        date = serializers.DateField(format="%Y-%m-%d")
        rama = serializers.PrimaryKeyRelatedField(queryset=Rama.objects.all())


    class CashRecordSerializer(serializers.ModelSerializer):
        class Meta:
            model = CashRecord
            fields = ['created_at', 'amount', 'note', 'record_type']


    class SaleSimpleCashSerializer(serializers.ModelSerializer):
        seller_name = serializers.ReadOnlyField()

        class Meta:
            model = Sale
            fields = ['client', 'selling_total_cash', 'seller_name', 'seller_fee', 'kladman_fee', 
                'loader_fee', 'delivery_fee']


    class CanSeeRamaDailyCashReportPermissions(permissions.BasePermission):
        def has_permission(self, request, view):
            if request.method in permissions.SAFE_METHODS:
                acc = request.user.account
                rama = request.GET.get('rama')
                can_see_ramas_list = acc.can_see_rama_daily_cash_report.all().values_list('pk', flat=True)

                if rama and (int(rama)) in can_see_ramas_list:
                    return True
            return False

    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, CanSeeRamaDailyCashReportPermissions]

    def get(self, request, format=None):
        data = dict()
        serializer = self.DateSerializer(data={'date': request.GET.get('date'), 
            'rama': request.GET.get('rama')})
        if serializer.is_valid():
            records = CashRecord.objects.filter(created_at__date=serializer.validated_data['date'],
             rama=serializer.validated_data['rama'])
            data['records'] = self.CashRecordSerializer(records, many=True).data
            data['income_records'] = self.CashRecordSerializer(records.filter(record_type='sale_income'),
                 many=True).data
            data['income_records_total'] = records.filter(record_type='sale_income').calc_sum()
            data['expense_records'] = self.CashRecordSerializer(
                records.filter(Q(record_type='rama_expenses') | Q(record_type='withdraw_employee')),
                 many=True).data
            data['expense_records_total'] = records.filter(
                Q(record_type='rama_expenses') | Q(record_type='withdraw_employee')).calc_sum()
            data['records_total'] = records.calc_sum_incomes_expenses()

            sales = Sale.objects.filter(date__date=serializer.validated_data['date'],
                rama=serializer.validated_data['rama'])
            data['sales'] = self.SaleSimpleCashSerializer(sales, many=True).data
            data['sales_totals'] = sales.calc_totals()

            data['sales_sellers_fee'] = [
                {'name': 'Сергей', 'total': sales.filter(seller__account__nickname='Сергей') \
                .aggregate(sum_seller_fee=Sum('seller_fee'))['sum_seller_fee']},
                {'name': 'Дарима', 'total': sales.filter(seller__account__nickname='Дарима') \
                .aggregate(sum_seller_fee=Sum('seller_fee'))['sum_seller_fee']}
            ]

            return Response(data)
        else:
            return Response({'message': 'Неверная дата.'}, status=status.HTTP_400_BAD_REQUEST)


class SaleCalcDataView(APIView):

    class LumberSimpleSerializer(serializers.ModelSerializer):
        lumber = serializers.ReadOnlyField(source='pk')

        class Meta:
            model = Lumber
            fields = ['name', 'lumber_type', 'wood_species', 'id', 'lumber', 'round_volume']


    class LumberSerializer(serializers.ModelSerializer):
        quantity = serializers.IntegerField(default=0)
        volume_total = serializers.FloatField(default=0)
        lumber = serializers.ReadOnlyField(source='pk')
        rama_price = serializers.ReadOnlyField(source='market_cost')
        selling_price = serializers.ReadOnlyField(source='market_cost')
        selling_total_cash = serializers.ReadOnlyField(source='market_cost')
        calc_type = serializers.CharField(default='exact')

        class Meta:
            model = Lumber
            exclude = ['created_at', 'modified_at', 'employee_rate', 'market_cost']

    def get(self, request):
        return Response({
            'pine_brus_lumbers': self.LumberSimpleSerializer(
                Lumber.objects.filter(lumber_type='brus', wood_species='pine'), many=True).data,
            'pine_doska_lumbers': self.LumberSimpleSerializer(
                Lumber.objects.filter(lumber_type='doska', wood_species='pine'), many=True).data,
            'lumbers': self.LumberSerializer(
                Lumber.objects.all(), many=True).data,
            }, status=status.HTTP_200_OK)


# resaws list
class ResawListView(generics.ListAPIView):

    class ReSawSerializer(serializers.ModelSerializer):
        lumber_in = serializers.ReadOnlyField(source='lumber_in.lumber.name')
        lumber_in_quantity = serializers.ReadOnlyField(source='lumber_in.quantity')
        lumber_in_wood_species = serializers.ReadOnlyField(source='lumber_in.lumber.wood_species')

        lumber_out = serializers.ReadOnlyField(source='lumber_out.lumber.name')
        lumber_out_quantity = serializers.ReadOnlyField(source='lumber_out.quantity')
        lumber_out_wood_species = serializers.ReadOnlyField(source='lumber_out.lumber.wood_species')

        who = serializers.ReadOnlyField(source='initiator.account.nickname')

        class Meta:
            model = ReSaw
            fields = ['id', 'created_at', 'lumber_in', 'lumber_in_quantity', 'lumber_out', 
                'lumber_out_quantity', 'who', 'lumber_in_wood_species', 'lumber_out_wood_species']


    class ResawFilter(filters.FilterSet):
        date = filters.DateFromToRangeFilter()

        class Meta:
            model = ReSaw
            fields = ['rama', 'date',]


    class CanSeeRamaResawPermissions(permissions.BasePermission):
        def has_permission(self, request, view):
            if request.method in permissions.SAFE_METHODS:
                acc = request.user.account
                rama = request.GET.get('rama')
                can_see_ramas_list = acc.can_see_rama_resaws.all().values_list('pk', flat=True)

                if rama and (int(rama)) in can_see_ramas_list:
                    return True
            return False

    queryset = ReSaw.objects.all()
    serializer_class = ReSawSerializer
    permission_classes = [IsAuthenticated, CanSeeRamaResawPermissions]
    filter_class = ResawFilter


# raw timber income
class IncomeTimberListView(generics.ListAPIView):

    class IncomeTimberSerializer(serializers.ModelSerializer):

        class TimberRecordSerializer(serializers.ModelSerializer):
            timber = serializers.StringRelatedField()
            wood_species = ChoiceField(source='timber.wood_species', read_only=True,
             choices=Timber.SPECIES)

            class Meta:
                model = TimberRecord
                fields = ['timber', 'quantity', 'volume', 'wood_species']

        who = serializers.ReadOnlyField(source='initiator.account.nickname')
        timber_records = TimberRecordSerializer(many=True)

        class Meta:
            model = IncomeTimber
            fields = ['id', 'created_at', 'who', 'quantity', 'volume', 'note', 'timber_records']


    class IncomeTimberFilter(filters.FilterSet):
        created_at = filters.DateFromToRangeFilter()

        class Meta:
            model = IncomeTimber
            fields = ['rama', 'created_at',]


    class CanSeeRamaIncomeTimberPermissions(permissions.BasePermission):
        def has_permission(self, request, view):
            if request.method in permissions.SAFE_METHODS:
                acc = request.user.account
                rama = request.GET.get('rama')
                can_see_ramas_list = acc.can_see_rama_raw_stock.all().values_list('pk', flat=True)

                if rama and (int(rama)) in can_see_ramas_list:
                    return True
            return False

    queryset = IncomeTimber.objects.all()
    serializer_class = IncomeTimberSerializer
    permission_classes = [IsAuthenticated, CanSeeRamaIncomeTimberPermissions]
    filter_class = IncomeTimberFilter


class QuotasPageView(APIView):

    class CashRecordSerializer(serializers.ModelSerializer):
        record_type = ChoiceField(read_only=True, choices=CashRecord.RECORD_TYPES)
        who = serializers.ReadOnlyField(source='initiator.account.nickname')

        class Meta:
            model = CashRecord
            fields = ['created_at', 'amount', 'note', 'record_type', 'who', 'id']
    
    # permission_classes = [IsAuthenticated, CanSeeRamaIncomeTimberPermissions]

    def get(self, request, format=None):
        data = dict()

        rama = Rama.objects.get(pk=request.GET.get('rama'))
        pine_data = Quota.objects.curent_rama_quota(rama=rama, wood_species='pine')
        larch_data = Quota.objects.curent_rama_quota(rama=rama, wood_species='larch')

        data['pine_data'] = pine_data
        data['larch_data'] = larch_data

        cash_records = CashRecord.objects.filter(rama=rama) \
                        .filter(Q(record_type='withdraw_cash_from_manager') |
                                Q(record_type='income_timber')) \
                        .order_by('-created_at')

        data['cash_records'] = self.CashRecordSerializer(cash_records, many=True).data
        data['manager_balance'] = cash_records.calc_manager_balance()

        return Response(data, status=status.HTTP_200_OK)


class Test1CView(APIView):
    permission_classes = [AllowAny,]

    def get(self, request, format=None):
        data = dict()
        data['hui'] = 'pizda'
        return Response(data, status=status.HTTP_200_OK)