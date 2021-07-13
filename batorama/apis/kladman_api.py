# # -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db.models import Q, Sum
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework import status, generics, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import serializers
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from django_filters import rest_framework as filters

from core.serializers import ChoiceField
from stock.models import Sale, LumberRecord, Lumber, ReSaw, RefuseLumber
from accounts.models import Account
from cash.models import CashRecord


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


class SaleLumberRecordSerializer(serializers.ModelSerializer):
    lumber = serializers.StringRelatedField()
    wood_species = ChoiceField(source='lumber.wood_species', read_only=True, choices=Lumber.SPECIES)
    
    class Meta:
        model = LumberRecord
        fields = ['lumber', 'quantity', 'volume', 'selling_price', 'selling_total_cash',
         'rama_price', 'rama_total_cash', 'wood_species']


class SaleView(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleReadSerializer
    # permission_classes = [IsAdminUser]

    class SaleReadSerializer(serializers.ModelSerializer):
        lumber_records = SaleLumberRecordSerializer(many=True)
        initiator = serializers.ReadOnlyField(source='initiator.account.nickname')
        seller_name = serializers.ReadOnlyField()
        date = serializers.DateTimeField(format='%d/%m', read_only=True)

        class Meta:
            model = Sale
            exclude = ['created_at', 'modified_at']

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
        kladman = User.objects.filter(account__is_kladman=True,
             account__rama=request.user.account.rama).first()
        kladman_id = kladman.pk if kladman else None

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
            'sellers': SellerSerializer(User.objects.filter(account__is_seller=True), many=True).data,
            'kladman_id': kladman_id
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
        sale = self.get_object()
        sale.delete()
        queryset = Sale.objects.filter(rama=request.user.account.rama)
        return Response({
            'sales': self.SaleReadSerializer(queryset, many=True).data,
            'totals': queryset.calc_totals()
            },
            status=status.HTTP_200_OK)


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
    created_at = filters.DateFromToRangeFilter()

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
                initiator=request.user
                )

            records = CashRecord.objects.filter(created_at__date=timezone.now()) \
                .filter(Q(record_type='rama_expenses') | Q(record_type='withdraw_employee'))

            return Response({
                'expense': CashRecordSerializer(cash_record).data,
                'records': CashRecordSerializer(records, many=True).data,
                'total': records.calc_sum(),
                'message': 'Успешно'
                },
                 status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





# resaw
class ReSawSerializer(serializers.ModelSerializer):
    lumber_in = serializers.ReadOnlyField(source='lumber_in.lumber.name')
    lumber_in_quantity = serializers.ReadOnlyField(source='lumber_in.quantity')

    lumber_out = serializers.ReadOnlyField(source='lumber_out.lumber.name')
    lumber_out_quantity = serializers.ReadOnlyField(source='lumber_out.quantity')

    class Meta:
        model = ReSaw
        fields = ['id', 'created_at', 'lumber_in', 'lumber_in_quantity', 'lumber_out', 
            'lumber_out_quantity']


class CreateReSawSerializer(serializers.Serializer):
    lumber_in = serializers.PrimaryKeyRelatedField(queryset=Lumber.objects.all())
    lumber_in_quantity = serializers.IntegerField()

    lumber_out = serializers.PrimaryKeyRelatedField(queryset=Lumber.objects.all())
    lumber_out_quantity = serializers.IntegerField()

    class Meta:
        model = ReSaw
        fields = ['id', 'created_at', 'lumber_in', 'lumber_in_quantity', 'lumber_out', 
            'lumber_out_quantity']


class ReSawViewSet(viewsets.ModelViewSet):
    queryset = ReSaw.objects.all()
    serializer_class = ReSawSerializer

    def create(self, request, serializer_class=CreateReSawSerializer):
        serializer = CreateReSawSerializer(data=request.data)
        if serializer.is_valid():
            resaw = ReSaw.objects.create_resaw(
                resaw_lumber_in={'lumber': serializer.validated_data['lumber_in'],
                    'quantity': serializer.validated_data['lumber_in_quantity']},
                resaw_lumber_out={'lumber': serializer.validated_data['lumber_out'],
                    'quantity': serializer.validated_data['lumber_out_quantity']},
                rama=request.user.account.rama,
                initiator=request.user
                )
            # resaws = ReSaw.objects.filter()
            return Response({
                'created': ReSawSerializer(resaw).data,
                # 'records': ReSawSerializer(records, many=True).data,
                'message': 'Успешно'
                },
                 status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# refuse
# class RefuseLumberSerializer(serializers.ModelSerializer):
#     lumber_name = serializers.ReadOnlyField(source='lumber.name')

#     class Meta:
#         model = ReSaw
#         fields = ['id', 'created_at', 'lumber', 'lumber_name', 'initiator' ]


# class RefuseLumberViewSet(viewsets.ModelViewSet):
#     queryset = ReSaw.objects.all()
#     serializer_class = RefuseLumberSerializer

#     def create(self, request):
#         serializer = RefuseLumberSerializer(data=request.data)
#         if serializer.is_valid():
#             refuse = RefuseLumber.objects.create_resaw(
#                 resaw_lumber_in={'lumber': serializer.validated_data['lumber_in'],
#                     'quantity': serializer.validated_data['lumber_in_quantity']},
#                 resaw_lumber_out={'lumber': serializer.validated_data['lumber_out'],
#                     'quantity': serializer.validated_data['lumber_out_quantity']},
#                 rama=request.user.account.rama,
#                 initiator=request.user
#                 )
#             # resaws = ReSaw.objects.filter()
#             return Response({
#                 'created': ReSawSerializer(resaw).data,
#                 # 'records': ReSawSerializer(records, many=True).data,
#                 'message': 'Успешно'
#                 },
#                  status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)