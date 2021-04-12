# # -*- coding: utf-8 -*-
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import serializers

from stock.models import Shift, LumberRecord, Employee, Lumber
from stock.testing_utils import create_init_data


class InitTestDataView(APIView):
    def get(self, request, format=None):
        create_init_data()
        return Response({'msg': 'Done.'})


class ShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = '__all__'


class RawLumberRecordSerializer(serializers.Serializer):
    lumber = serializers.PrimaryKeyRelatedField(queryset=Lumber.objects.all())
    quantity = serializers.IntegerField()
    volume = serializers.FloatField()
    employee_rate = serializers.IntegerField()
    total = serializers.IntegerField()


class ShiftCreateSerializer(serializers.ModelSerializer):
    employees = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(), many=True)
    raw_records = RawLumberRecordSerializer(many=True)

    class Meta:
        model = Shift
        fields = ('date', 'shift_type', 'employees', 'raw_records')


class LumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lumber
        exclude = ['created_at', 'modified_at']


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
    def lumbers(self, request):
        return Response(LumberSerializer(Lumber.objects.all(), many=True).data,
            status=status.HTTP_200_OK)