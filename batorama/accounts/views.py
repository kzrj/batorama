# # -*- coding: utf-8 -*-
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import serializers

from accounts.models import Account, CashRecord


class RamshikWithCashSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'nickname', 'cash']


class CreateRamshikPayoutSerializer(serializers.Serializer):
    employee = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())
    amount = serializers.IntegerField()


class LastPayoutsSerializer(serializers.ModelSerializer):
    employee = serializer.ReadOnlyField(source='account.nickname')

    class Meta:
        model = CashRecord
        fields = ['id', 'amount', 'record_type', 'created_at','employee']


class RamshikiPaymentViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'])
    def init_data(self, request, pk=None):
        return Response({
            'employees': RamshikWithCashSerializer(
                Account.objects.filter(is_ramshik=True), many=True).data,
            'last_payouts': LastPayoutsSerializer(CashRecord.objects.all(), many=True).data
            },
                status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def ramshik_payout(self, request, pk=None):
        serializer = CreateRamshikPayoutSerializer(data=request.data)
        if serializer.is_valid():
            CashRecord.objects.create_withdraw_employee(
                employee=serializer.validated_data['employee'],
                amount=serializer.validated_data['amount'],
                initiator=request.user
                )
            return Response({
                'employees': RamshikWithCashSerializer(
                    Account.objects.filter(is_ramshik=True), many=True).data,
                'last_payouts': LastPayoutsSerializer(CashRecord.objects.all(), many=True).data,
                'message': 'Успешно',
                },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
