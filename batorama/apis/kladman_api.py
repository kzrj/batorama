# # -*- coding: utf-8 -*-
from rest_framework import status, generics, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import serializers

from stock.models import Sale, LumberRecord, Lumber
from accounts.models import Account


class LumberRecordSerializer(serializers.ModelSerializer):
    lumber = serializers.StringRelatedField()

    class Meta:
        model = LumberRecord
        fields = ('lumber', 'quantity', 'volume', 'rate', 'total_cash', 'back_total_cash')


class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = '__all__'


class SaleReadSerializer(serializers.ModelSerializer):
    lumber_records = LumberRecordSerializer(many=True)

    class Meta:
        model = Sale
        fields = '__all__'


class RawLumberRecordSerializer(serializers.Serializer):
    lumber = serializers.PrimaryKeyRelatedField(queryset=Lumber.objects.all())
    quantity = serializers.IntegerField()
    volume_total = serializers.FloatField()
    rate = serializers.IntegerField()
    cash = serializers.FloatField()


class SaleCreateSerializer(serializers.ModelSerializer):
    raw_records = RawLumberRecordSerializer(many=True)

    class Meta:
        model = Sale
        fields = ('date', 'raw_records', 'cash', 'volume', 'add_expenses', 'note')


class LumberSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(default=0)
    volume_total = serializers.FloatField(default=0)
    cash = serializers.FloatField(default=0)
    rate = serializers.FloatField(default=0)
    lumber = serializers.ReadOnlyField(source='pk')

    class Meta:
        model = Lumber
        exclude = ['created_at', 'modified_at', 'employee_rate']


class LumberSimpleSerializer(serializers.ModelSerializer):
    lumber = serializers.ReadOnlyField(source='pk')

    class Meta:
        model = Lumber
        fields = ['name', 'lumber_type', 'wood_species', 'id', 'lumber']



class SaleList(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    # permission_classes = [IsAdminUser]

    def create(self, request):
        serializer = SaleCreateSerializer(data=request.data)
        if serializer.is_valid():
            sale = Sale.objects.create_sale_raw_records(
                date=serializer.validated_data.get('date'),
                raw_records=serializer.validated_data['raw_records'],
                cash=serializer.validated_data['cash'],
                volume=serializer.validated_data['volume'],
                add_expenses=serializer.validated_data.get('add_expenses', 0),
                note=serializer.validated_data.get('note'),
                rama=request.user.account.rama,
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
            'larch_doska_lumbers': LumberSimpleSerializer(
                Lumber.objects.filter(lumber_type='doska', wood_species='larch'), many=True).data,
            'lumbers': LumberSerializer(
                Lumber.objects.all(), many=True).data,
            }, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass
