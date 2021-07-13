# # -*- coding: utf-8 -*-
from rest_framework import status, viewsets, generics, permissions, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from stock.models import Shift, LumberRecord, Lumber
from stock.testing_utils import create_init_data
from rawstock.testing_utils import create_test_timber
from accounts.models import Account
from cash.models import CashRecord


class InitTestDataView(APIView):
    def get(self, request, format=None):
        # create_init_data()
        create_test_timber()
        return Response({'msg': 'Done.'})


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

    queryset = Shift.objects.all()
    serializer_class = ShiftReadSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = self.filter_queryset(request.user.account.shift_set.all() \
            .select_related('initiator__account') \
            .prefetch_related('lumber_records__lumber', 'employees',) \
            .order_by('-created_at'))
                
        serializer = self.ShiftReadSerializer(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.ShiftReadSerializer(queryset, many=True)
            return self.get_paginated_response(serializer.data)

        return super().list(request)


class RamshikPayoutView(APIView):

    class RamshikWithCashSerializer(serializers.ModelSerializer):
        class Meta:
            model = Account
            fields = ['id', 'nickname', 'cash']


    class LastPayoutsSerializer(serializers.ModelSerializer):
        employee = serializers.ReadOnlyField(source='account.nickname')

        class Meta:
            model = CashRecord
            fields = ['id', 'amount', 'record_type', 'created_at', 'employee']


    def get(self, request):
        ramshik = request.user.account
        return Response({
            'ramshik': self.RamshikWithCashSerializer(ramshik).data,
            'last_payouts': self.LastPayoutsSerializer(
                CashRecord.objects.filter(account=ramshik).order_by('-created_at'), many=True).data
            },
                status=status.HTTP_200_OK)