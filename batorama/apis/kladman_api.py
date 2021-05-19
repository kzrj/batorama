# # -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone

from rest_framework import status, generics, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import serializers

from django_filters import rest_framework as filters

from stock.models import Sale, LumberRecord, Lumber
from accounts.models import Account
from cash.models import CashRecord

# Create sale kladman

class LumberRecordSerializer(serializers.ModelSerializer):
    volume_total = serializers.ReadOnlyField(source='volume')
    name = serializers.ReadOnlyField(source='lumber.name')
    selling_total_cash = serializers.ReadOnlyField(source='lumber.name')
    china_name = serializers.ReadOnlyField()

    class Meta:
        model = LumberRecord
        fields = ('name', 'quantity', 'volume_total', 'selling_total_cash', 'selling_price',
         'china_name')


class SaleReadSerializer(serializers.ModelSerializer):
    lumber_records = LumberRecordSerializer(many=True)

    class Meta:
        model = Sale
        fields = '__all__'


class RawLumberRecordSerializer(serializers.Serializer):
    lumber = serializers.PrimaryKeyRelatedField(queryset=Lumber.objects.all())
    quantity = serializers.IntegerField()
    rama_price = serializers.IntegerField()
    selling_price = serializers.IntegerField()
    selling_total_cash = serializers.IntegerField()
    calc_type = serializers.CharField()


class SaleCreateSerializer(serializers.ModelSerializer):
    raw_records = RawLumberRecordSerializer(many=True)
    loader = serializers.BooleanField()

    class Meta:
        model = Sale
        fields = ('date', 'raw_records', 'seller', 'bonus_kladman', 'client', 'loader',
         'delivery_fee', )


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


class LumberSimpleSerializer(serializers.ModelSerializer):
    lumber = serializers.ReadOnlyField(source='pk')

    class Meta:
        model = Lumber
        fields = ['name', 'lumber_type', 'wood_species', 'id', 'lumber', 'round_volume']


class SellerSerializer(serializers.ModelSerializer):
    nickname = serializers.ReadOnlyField(source='account.nickname')

    class Meta:
        model = User
        fields = ['id', 'nickname']


class SaleView(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleReadSerializer
    # permission_classes = [IsAdminUser]

    def list(self, request):
        pass

    def create(self, request, serializer_class=SaleCreateSerializer):
        serializer = SaleCreateSerializer(data=request.data)
        if serializer.is_valid():
            sale = Sale.objects.create_sale_common(
                date=serializer.validated_data.get('date'),
                raw_records=serializer.validated_data['raw_records'],
                loader=serializer.validated_data['loader'],
                delivery_fee=serializer.validated_data['delivery_fee'],
                # add_expenses=serializer.validated_data['add_expenses'],
                # note=serializer.validated_data['note'],
                client=serializer.validated_data['client'],
                seller=serializer.validated_data['seller'],
                bonus_kladman=serializer.validated_data['bonus_kladman'],
                initiator=request.user,
                )
            
            return Response({
                'sale': SaleReadSerializer(sale).data,
                'message': 'Успешно'
                },
                 status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False)
    def sale_create_data(self, request):
        return Response({
            'pine_brus_lumbers': LumberSimpleSerializer(
                Lumber.objects.filter(lumber_type='brus', wood_species='pine'), many=True).data,
            'larch_brus_lumbers': LumberSimpleSerializer(
                Lumber.objects.filter(lumber_type='brus', wood_species='larch'), many=True).data,
            'pine_doska_lumbers': LumberSimpleSerializer(
                Lumber.objects.filter(lumber_type='doska', wood_species='pine'), many=True).data,
            'lumbers': LumberSerializer(
                Lumber.objects.all(), many=True).data,
            'sellers': SellerSerializer(User.objects.filter(account__is_seller=True), many=True).data,
            'kladman_id': User.objects.filter(
                account__is_kladman=True, account__rama=request.user.account.rama).first().pk
            }, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def sale_calc_data(self, request):
        return Response({
            'pine_brus_lumbers': LumberSimpleSerializer(
                Lumber.objects.filter(lumber_type='brus', wood_species='pine'), many=True).data,
            'pine_doska_lumbers': LumberSimpleSerializer(
                Lumber.objects.filter(lumber_type='doska', wood_species='pine'), many=True).data,
            'lumbers': LumberSerializer(
                Lumber.objects.all(), many=True).data,
            }, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass


# Create cash_records

class CashRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashRecord
        fields = ['created_at', 'amount', 'note', 'record_type']


class CashRecordCreateExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashRecord
        fields = ['amount', 'note']


class ExpensesFilter(filters.FilterSet):
    date = filters.DateFromToRangeFilter()

    class Meta:
        model = CashRecord
        fields = '__all__'


class CashRecordsView(viewsets.ModelViewSet):
    queryset = CashRecord.objects.all()
    serializer_class = CashRecordSerializer
    filter_class = ExpensesFilter
    # permission_classes = [IsAdminUser]

    @action(methods=['post'], detail=False)
    def create_expense(self, request, serializer_class=CashRecordCreateExpenseSerializer):
        serializer = CashRecordCreateExpenseSerializer(data=request.data)
        if serializer.is_valid():
            cash_record = CashRecord.objects.create_rama_expense(
                amount=serializer.validated_data['amount'],
                note=serializer.validated_data['note'],
                rama=request.user.account.rama,
                initiator=request.user
                )

            return Response({
                'expense': CashRecordSerializer(cash_record).data,
                'expenses': CashRecordSerializer(
                    CashRecord.objects.filter(
                        created_at__date=timezone.now()),
                        many=True).data,
                'message': 'Успешно'
                },
                 status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)