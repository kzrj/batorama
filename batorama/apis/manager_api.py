# # -*- coding: utf-8 -*-
from rest_framework import status, viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated

from django_filters import rest_framework as filters

from accounts.models import Account
from cash.models import CashRecord
from stock.models import Shift, LumberRecord, Lumber, Sale
from core.serializers import AnnotateFieldsModelSerializer


class RamshikWithCashSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'nickname', 'cash']


class CreateRamshikPayoutSerializer(serializers.Serializer):
    employee = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())
    amount = serializers.IntegerField()


class LastPayoutsSerializer(serializers.ModelSerializer):
    employee = serializers.ReadOnlyField(source='account.nickname')

    class Meta:
        model = CashRecord
        fields = ['id', 'amount', 'record_type', 'created_at', 'employee']


class RamshikiPaymentViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'])
    def init_data(self, request, pk=None):
        return Response({
            'employees': RamshikWithCashSerializer(
                Account.objects.filter(is_ramshik=True).order_by('nickname'), many=True).data,
            'last_payouts': LastPayoutsSerializer(
                CashRecord.objects.all().order_by('-created_at')[:10], many=True).data
            },
                status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def ramshik_payout(self, request, pk=None):
        serializer = CreateRamshikPayoutSerializer(data=request.data)
        if serializer.is_valid():
            CashRecord.objects.create_withdraw_employee(
                employee=serializer.validated_data['employee'],
                amount=serializer.validated_data['amount'],
                note=f'выдача зп рамщику {serializer.validated_data["employee"].nickname}',
                initiator=request.user
                )
            return Response({
                'employees': RamshikWithCashSerializer(
                    Account.objects.filter(is_ramshik=True).order_by('nickname'),
                    many=True).data,
                'last_payouts': LastPayoutsSerializer(
                    CashRecord.objects.all().order_by('-created_at')[:10], many=True).data,
                'message': 'Успешно',
                },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LumberRecordSerializer(serializers.ModelSerializer):
    lumber = serializers.StringRelatedField()
    
    class Meta:
        model = LumberRecord
        fields = ['lumber', 'quantity', 'volume', 'rate']


class ShiftSerializer(serializers.ModelSerializer):
    employees = serializers.StringRelatedField(many=True)
    lumber_records = LumberRecordSerializer(many=True)
    initiator = serializers.ReadOnlyField(source='initiator.account.nickname')
    date = serializers.DateTimeField(format='%d/%m', read_only=True)

    class Meta:
        model = Shift
        exclude = ['created_at', 'modified_at']


class ShiftListView(generics.ListAPIView):
    queryset = Shift.objects.all() \
        .select_related('initiator__account') \
        .prefetch_related('lumber_records__lumber', 'employees',)
    serializer_class = ShiftSerializer
    permission_classes = [IsAuthenticated]


class LumberStockReadSerializer(AnnotateFieldsModelSerializer):
    stock_total_cash = serializers.ReadOnlyField()
    
    class Meta:
        model = Lumber
        fields = '__all__'


class LumberStockListView(generics.ListAPIView):
    queryset = Lumber.objects.all() \
        .prefetch_related('records', )
    serializer_class = LumberStockReadSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        rama = request.user.account.rama
        queryset = self.filter_queryset(
            self.queryset.add_rama_current_stock(rama=rama)
            )
                
        serializer = LumberStockReadSerializer(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = LumberStockReadSerializer(queryset, many=True)
            return self.get_paginated_response(serializer.data)

        return super().list(request)


class SaleLumberRecordSerializer(serializers.ModelSerializer):
    lumber = serializers.StringRelatedField()
    
    class Meta:
        model = LumberRecord
        fields = ['lumber', 'quantity', 'volume', 'selling_price', 'selling_total_cash',
         'rama_price', 'rama_total_cash']


class SaleReadSerializer(serializers.ModelSerializer):
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
        fields = '__all__'


class SaleListView(generics.ListAPIView):
    queryset = Sale.objects.all() \
        .select_related('initiator__account') \
        .prefetch_related('lumber_records__lumber',)
    serializer_class = SaleReadSerializer
    permission_classes = [IsAuthenticated]
    filter_class = SaleFilter

    def list(self, request):
        data = dict()
        rama = request.user.account.rama
        queryset = self.filter_queryset(
            self.queryset.filter(rama=rama)
            )
                
        serializer = SaleReadSerializer(queryset, many=True)
        data['sales'] = serializer.data
        data['totals'] = queryset.calc_totals()

        return Response(data)

    # def list(self, request):
    #     rama = request.user.account.rama
    #     queryset = self.filter_queryset(
    #         self.queryset.filter(rama=rama)
    #         )
                
    #     serializer = SaleReadSerializer(queryset, many=True)

    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = SaleReadSerializer(queryset, many=True)
    #         return self.get_paginated_response(serializer.data)

    #     return super().list(request)