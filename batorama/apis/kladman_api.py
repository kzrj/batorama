# # -*- coding: utf-8 -*-
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import serializers

from stock.models import Sale, LumberRecord, Lumber
from accounts.models import Account


class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = '__all__'


class RawLumberRecordSerializer(serializers.Serializer):
    lumber = serializers.PrimaryKeyRelatedField(queryset=Lumber.objects.all())
    quantity = serializers.IntegerField()
    volume_total = serializers.FloatField()
    rate = serializers.IntegerField()
    cash = serializers.FloatField()


class SeleCreateSerializer(serializers.ModelSerializer):
    raw_records = RawLumberRecordSerializer(many=True)

    class Meta:
        model = Shift
        fields = ('date', 'raw_records')


class LumberSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(default=0)
    volume_total = serializers.FloatField(default=0)
    cash = serializers.FloatField(default=0)

    class Meta:
        model = Lumber
        exclude = ['created_at', 'modified_at']


class RamshikSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'nickname']


class ShiftViewSet(viewsets.ModelViewSet):
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer

    def create(self, request):
        serializer = ShiftCreateSerializer(data=request.data)
        if serializer.is_valid():
            shift = Shift.objects.create_shift_raw_records(
                date=serializer.validated_data.get('date'),
                shift_type=serializer.validated_data['shift_type'],
                employees=serializer.validated_data['employees'],
                raw_records=serializer.validated_data['raw_records'],
                initiator=request.user,
                )
            
            return Response(ShiftSerializer(shift).data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False)
    def shift_create_data(self, request):
        return Response({
            'lumbers': LumberSerializer(Lumber.objects.all(), many=True).data,
            'employees': RamshikSerializer(Account.objects.filter(is_ramshik=True), many=True).data,
            }, status=status.HTTP_200_OK)