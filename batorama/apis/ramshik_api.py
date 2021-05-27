# # -*- coding: utf-8 -*-
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import serializers

from stock.models import Shift, LumberRecord, Lumber
from stock.testing_utils import create_init_data
from accounts.models import Account
from cash.models import CashRecord


class InitTestDataView(APIView):
    def get(self, request, format=None):
        create_init_data()
        return Response({'msg': 'Done.'})


class LumberRecordSerializer(serializers.ModelSerializer):
    lumber = serializers.StringRelatedField()

    class Meta:
        model = LumberRecord
        fields = ('lumber', 'quantity', 'volume', 'rate', 'total_cash', 'back_total_cash')


class ShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = '__all__'


class ShiftReadSerializer(serializers.ModelSerializer):
    lumber_records = LumberRecordSerializer(many=True)
    employees = serializers.StringRelatedField(read_only=True, many=True)
    date = serializers.DateTimeField(format='%d/%m', read_only=True)

    class Meta:
        model = Shift
        fields = '__all__'


class RawLumberRecordSerializer(serializers.Serializer):
    lumber = serializers.PrimaryKeyRelatedField(queryset=Lumber.objects.all())
    quantity = serializers.IntegerField()
    volume_total = serializers.FloatField()
    employee_rate = serializers.IntegerField()
    cash = serializers.FloatField()


class ShiftCreateSerializer(serializers.ModelSerializer):
    employees = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all(), many=True)
    raw_records = RawLumberRecordSerializer(many=True)

    class Meta:
        model = Shift
        fields = ('date', 'shift_type', 'employees', 'raw_records', 'employee_cash', 'volume', 'note')


class LumberSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(default=0)
    volume_total = serializers.FloatField(default=0)
    cash = serializers.FloatField(default=0)

    class Meta:
        model = Lumber
        exclude = ['created_at', 'modified_at', 'china_height', 'china_length', 'china_volume',
         'china_width', 'round_volume', 'height', 'width', 'length', 'lumber_type']


class RamshikSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'nickname']


class ShiftViewSet(viewsets.ModelViewSet):
    queryset = Shift.objects.all()\
        .select_related('initiator__account') \
        .prefetch_related('lumber_records__lumber', 'employees',)
    serializer_class = ShiftReadSerializer

    def list(self, request):
        queryset = self.filter_queryset(request.user.account.shift_set.all())
                
        serializer = ShiftReadSerializer(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ShiftReadSerializer(queryset, many=True)
            return self.get_paginated_response(serializer.data)

        return super().list(request)

    def create(self, request):
        serializer = ShiftCreateSerializer(data=request.data)
        if serializer.is_valid():
            shift = Shift.objects.create_shift_raw_records(
                date=serializer.validated_data.get('date'),
                shift_type=serializer.validated_data['shift_type'],
                employees=serializer.validated_data['employees'],
                raw_records=serializer.validated_data['raw_records'],
                cash=serializer.validated_data['employee_cash'],
                volume=serializer.validated_data['volume'],
                note=serializer.validated_data.get('note'),
                rama=request.user.account.rama,
                initiator=request.user,
                )
            
            return Response(ShiftReadSerializer(shift).data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False)
    def shift_create_data(self, request):
        # lumbers = Lumber.objects.exclude(lumber_type='doska', wood_species='larch')
        lumbers = Lumber.objects.all()
        return Response({
            'lumbers': LumberSerializer(lumbers, many=True).data,
            'employees': RamshikSerializer(Account.objects.filter(is_ramshik=True), many=True).data,
            }, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass


class RamshikWithCashSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'nickname', 'cash']


class LastPayoutsSerializer(serializers.ModelSerializer):
    employee = serializers.ReadOnlyField(source='account.nickname')

    class Meta:
        model = CashRecord
        fields = ['id', 'amount', 'record_type', 'created_at', 'employee']


class RamshikPayoutViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'])
    def get_data(self, request, pk=None):
        ramshik = request.user.account
        return Response({
            'ramshik': RamshikWithCashSerializer(ramshik).data,
            'last_payouts': LastPayoutsSerializer(
                CashRecord.objects.filter(account=ramshik).order_by('-created_at'), many=True).data
            },
                status=status.HTTP_200_OK)