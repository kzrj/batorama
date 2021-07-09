# # -*- coding: utf-8 -*-
from django.contrib.auth.models import User

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated

from django_filters import rest_framework as filters

from stock.models import Lumber, Rama, LumberRecord, Shift, Sale
from cash.models import CashRecord 

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
                 'wood_species')

        lumber_records = LumberRecordSerializer(many=True)
        employees = serializers.StringRelatedField(read_only=True, many=True)
        date = serializers.DateTimeField(format='%d/%m', read_only=True)

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