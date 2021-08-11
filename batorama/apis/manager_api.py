# # -*- coding: utf-8 -*-
from django.db.models import Q
from django.contrib.auth.models import User
from django.utils import timezone

from rest_framework import status, viewsets, generics, serializers, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from django_filters import rest_framework as filters

from accounts.models import Account
from cash.models import CashRecord
from stock.models import Shift, LumberRecord, Lumber, Sale, Rama, ReSaw, LumberSawRate
from rawstock.models import IncomeTimber, Timber, TimberRecord, Quota

from core.serializers import AnnotateFieldsModelSerializer, ChoiceField


class SaleView(viewsets.ModelViewSet):

    class SaleReadSerializer(serializers.ModelSerializer):

        class SaleLumberRecordSerializer(serializers.ModelSerializer):
            lumber = serializers.StringRelatedField()
            wood_species = ChoiceField(source='lumber.wood_species', read_only=True, choices=Lumber.SPECIES)
            
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


    class SaleCreateSerializer(serializers.ModelSerializer):

        class RawLumberRecordSerializer(serializers.Serializer):
            lumber = serializers.PrimaryKeyRelatedField(queryset=Lumber.objects.all())
            quantity = serializers.IntegerField()
            rama_price = serializers.IntegerField()
            selling_price = serializers.IntegerField()
            selling_total_cash = serializers.IntegerField()
            calc_type = serializers.CharField()

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


    class LumberSawRateSerializer(serializers.ModelSerializer):
        lumber = serializers.ReadOnlyField(source='lumber.pk')
        id = serializers.ReadOnlyField(source='lumber.pk')
        name = serializers.ReadOnlyField(source='lumber.name')
        lumber_type = serializers.ReadOnlyField(source='lumber.lumber_type')    
        round_volume = serializers.ReadOnlyField(source='lumber.round_volume')
        wood_species = serializers.ReadOnlyField(source='lumber.wood_species')

        class Meta:
            model = LumberSawRate
            fields = ['name', 'lumber_type', 'wood_species', 'lumber', 'id', 'round_volume']


    class SellerSerializer(serializers.ModelSerializer):
        nickname = serializers.ReadOnlyField(source='account.nickname')

        class Meta:
            model = User
            fields = ['id', 'nickname']


    class OnlyManagerCanCreateDeletePermissions(permissions.BasePermission):
        def has_permission(self, request, view):
            if request.method in permissions.SAFE_METHODS:
                return True

            if request.method == 'POST' or request.method == 'DELETE':
                return request.user.account.is_manager

            return False

        def has_object_permission(self, request, view, obj):
            if request.method == 'DELETE':
                return request.user.account.rama == obj.rama

            return False

    queryset = Sale.objects.all()
    serializer_class = SaleReadSerializer
    permission_classes = [IsAuthenticated, OnlyManagerCanCreateDeletePermissions]

    def create(self, request, serializer_class=SaleCreateSerializer):
        serializer = self.SaleCreateSerializer(data=request.data)
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
                'sale': self.SaleReadSerializer(sale).data,
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
        lumber_rates = LumberSawRate.objects.filter(rama=request.user.account.rama) \
                                            .select_related('lumber')

        return Response({
            'pine_brus_lumbers': self.LumberSawRateSerializer(
                lumber_rates.filter(lumber__lumber_type='brus', lumber__wood_species='pine'), many=True).data,
            'larch_brus_lumbers': self.LumberSawRateSerializer(
                lumber_rates.filter(lumber__lumber_type='brus', lumber__wood_species='larch'), many=True).data,
            'pine_doska_lumbers': self.LumberSawRateSerializer(
                lumber_rates.filter(lumber__lumber_type='doska', lumber__wood_species='pine'), many=True).data,
            'larch_doska_lumbers': self.LumberSawRateSerializer(
                lumber_rates.filter(lumber__lumber_type='doska', lumber__wood_species='larch'), many=True).data,
            'lumbers': self.LumberSerializer(
                Lumber.objects.all(), many=True).data,
            'sellers': self.SellerSerializer(User.objects.filter(account__is_seller=True), many=True).data,
            'kladman_id': kladman_id
            }, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        sale = self.get_object()
        sale.delete()
        queryset = Sale.objects.filter(rama=request.user.account.rama)
        return Response({
            'sales': self.SaleReadSerializer(queryset, many=True).data,
            'totals': queryset.calc_totals()
            },
            status=status.HTTP_200_OK)


class ShiftViewSet(viewsets.ViewSet):

    class ShiftCreateSerializer(serializers.ModelSerializer):

        class RawLumberRecordSerializer(serializers.Serializer):
            lumber = serializers.PrimaryKeyRelatedField(queryset=Lumber.objects.all())
            quantity = serializers.IntegerField()
            volume_total = serializers.FloatField()
            employee_rate = serializers.IntegerField()
            cash = serializers.FloatField()

        employees = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all(), many=True)
        raw_records = RawLumberRecordSerializer(many=True)

        class Meta:
            model = Shift
            fields = ('date', 'shift_type', 'employees', 'raw_records', 'employee_cash', 'note')


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


    class LumberSerializer(serializers.ModelSerializer):
        quantity = serializers.IntegerField(default=0)
        volume_total = serializers.FloatField(default=0)
        cash = serializers.FloatField(default=0)

        class Meta:
            model = Lumber
            exclude = ['created_at', 'modified_at', 'china_height', 'china_length', 'china_volume',
             'china_width', 'round_volume', 'height', 'width', 'length']


    class LumberSawRateSerializer(serializers.ModelSerializer):
        id = serializers.ReadOnlyField(source='lumber.pk')
        name = serializers.ReadOnlyField(source='lumber.name')
        lumber_type = serializers.ReadOnlyField(source='lumber.lumber_type')
        quantity = serializers.IntegerField(default=0)
        volume = serializers.ReadOnlyField(source='lumber.volume')
        volume_total = serializers.FloatField(default=0)
        wood_species = serializers.ReadOnlyField(source='lumber.wood_species')
        cash = serializers.FloatField(default=0.0)

        class Meta:
            model = LumberSawRate
            fields = ['id', 'employee_rate', 'name', 'lumber_type', 'quantity', 'volume',
             'volume_total', 'wood_species', 'cash']


    class RamshikSerializer(serializers.ModelSerializer):
        class Meta:
            model = Account
            fields = ['id', 'nickname']


    class OnlyManagerCanCreatePermissions(permissions.BasePermission):
        def has_permission(self, request, view):
            if request.method in permissions.SAFE_METHODS:
                return request.user.account.is_manager

            if request.method == 'POST' or request.method == 'DELETE':
                return request.user.account.is_manager

            return False

        def has_object_permission(self, request, view, obj):
            if request.method == 'DELETE':
                return request.user.account.rama == obj.rama

            return False

    permission_classes = [IsAuthenticated, OnlyManagerCanCreatePermissions]

    def create(self, request):
        serializer = self.ShiftCreateSerializer(data=request.data)
        if serializer.is_valid():
            shift = Shift.objects.create_shift_raw_records(
                date=serializer.validated_data.get('date'),
                shift_type=serializer.validated_data['shift_type'],
                employees=serializer.validated_data['employees'],
                raw_records=serializer.validated_data['raw_records'],
                cash=serializer.validated_data['employee_cash'],
                note=serializer.validated_data.get('note'),
                rama=request.user.account.rama,
                initiator=request.user,
                )
            
            return Response(self.ShiftReadSerializer(shift).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False)
    def shift_create_data(self, request):
        lumber_rates = LumberSawRate.objects.filter(rama=request.user.account.rama) \
                                            .select_related('lumber')
        return Response({
            'lumbers': self.LumberSawRateSerializer(lumber_rates, many=True).data,
            'employees': self.RamshikSerializer(Account.objects.filter(is_ramshik=True,
                rama=request.user.account.rama), many=True).data,
            }, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        Shift.objects.get(pk=pk).delete()
        return Response({
            'shifts': self.ShiftReadSerializer(
                    Shift.objects.filter(rama=request.user.account.rama,
                     created_at__date__gte=timezone.now().date()), many=True).data,
            },
            status=status.HTTP_200_OK)


class RamshikiPaymentViewSet(viewsets.ViewSet):
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


    class CreateRamshikSerializer(serializers.Serializer):
        nickname = serializers.CharField()
        cash = serializers.IntegerField(default=0)

    
    class OnlyManagerCanCreatePermissions(permissions.BasePermission):
        def has_permission(self, request, view):
            if request.method in permissions.SAFE_METHODS:
                return request.user.account.is_manager

            if request.method == 'POST' or request.method == 'DELETE':
                return request.user.account.is_manager

            return False

        def has_object_permission(self, request, view, obj):
            if request.method == 'DELETE':
                return request.user.account.rama == obj.rama

            return False

    permission_classes = [IsAuthenticated, OnlyManagerCanCreatePermissions]

    def create(self, request):
        serializer = self.CreateRamshikSerializer(data=request.data)
        if serializer.is_valid():
            ramshik = Account.objects.create(
                nickname=serializer.validated_data['nickname'],
                cash=serializer.validated_data['cash'],
                is_ramshik=True,
                rama=request.user.account.rama,
                )
            
            return Response({'employees': self.RamshikWithCashSerializer(
                    Account.objects.filter(rama=request.user.account.rama, is_ramshik=True),
                     many=True).data}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def init_data(self, request, pk=None):
        return Response({
            'employees': self.RamshikWithCashSerializer(
                Account.objects.filter(is_ramshik=True, rama=request.user.account.rama)\
                    .order_by('nickname'), many=True).data,
            'last_payouts': self.LastPayoutsSerializer(
                CashRecord.objects.filter(Q(record_type='payout_to_employee_from_shift') |
                    Q(record_type='withdraw_employee')).filter(rama=request.user.account.rama) \
                    .order_by('-created_at')[:10], many=True).data
            },
                status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def ramshik_payout(self, request, pk=None):
        serializer = self.CreateRamshikPayoutSerializer(data=request.data)
        if serializer.is_valid():
            CashRecord.objects.create_withdraw_employee(
                employee=serializer.validated_data['employee'],
                amount=serializer.validated_data['amount'],
                note=f'выдача зп рамщику {serializer.validated_data["employee"].nickname}',
                initiator=request.user,
                )
            return Response({
                'employees': self.RamshikWithCashSerializer(
                    Account.objects.filter(is_ramshik=True, rama=request.user.account.rama)\
                        .order_by('nickname'),
                    many=True).data,
                'last_payouts': self.LastPayoutsSerializer(
                    CashRecord.objects.filter(Q(record_type='payout_to_employee_from_shift') |
                    Q(record_type='withdraw_employee')).filter(rama=request.user.account.rama) \
                        .order_by('-created_at')[:10], many=True).data,
                'message': 'Успешно',
                },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        Account.objects.get(pk=pk).delete()
        return Response({
            'employees': self.RamshikWithCashSerializer(
                    Account.objects.filter(rama=request.user.account.rama, is_ramshik=True),
                     many=True).data,
            },
            status=status.HTTP_200_OK)


class SetLumberMarketPriceView(APIView):
    # authentication_classes = [JSONWebTokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]

    class SetLumberMarketPriceSerializer(serializers.Serializer):
        lumber = serializers.PrimaryKeyRelatedField(queryset=Lumber.objects.all())
        market_cost = serializers.IntegerField()

    def post(self, request, format=None):
        serializer = self.SetLumberMarketPriceSerializer(data=request.data)

        if serializer.is_valid():
            lumber = serializer.validated_data['lumber']
            lumber.market_cost = serializer.validated_data['market_cost']
            lumber.save()

            return Response({
                'lumber': lumber.pk,
                'market_cost': lumber.market_cost,
                'message': 'Успешно изменено',
                },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Create cash_records
class CashRecordsView(viewsets.ModelViewSet):

    class CashRecordSerializer(serializers.ModelSerializer):

        class Meta:
            model = CashRecord
            fields = ['created_at', 'amount', 'note', 'record_type', 'id']


    class CashRecordCreateExpenseSerializer(serializers.ModelSerializer):
        class Meta:
            model = CashRecord
            fields = ['amount', 'note']


    class ExpensesFilter(filters.FilterSet):
        created_at = filters.DateFromToRangeFilter()

        class Meta:
            model = CashRecord
            fields = '__all__'


    class OnlyManagerCanCreateDeletePermissions(permissions.BasePermission):
        def has_permission(self, request, view):
            if request.method in permissions.SAFE_METHODS:
                return True

            if request.method == 'POST' or request.method == 'DELETE':
                return request.user.account.is_manager

            return False

        def has_object_permission(self, request, view, obj):
            if request.method == 'DELETE':
                return request.user.account.rama == obj.rama

            return False


    class BossOrCapoPermission(permissions.BasePermission):
        def has_permission(self, request, view):
            if request.method == 'POST':
                return request.user.account.is_boss or request.user.account.is_capo

            return False

    queryset = CashRecord.objects.all()
    serializer_class = CashRecordSerializer
    filter_class = ExpensesFilter
    permission_classes = [IsAuthenticated, OnlyManagerCanCreateDeletePermissions]

    def get_queryset(self):
        # all detail methods will not found if record is outside this queryset       
        return CashRecord.objects.filter(rama=self.request.user.account.rama)\
            .filter(Q(record_type='rama_expenses') | Q(record_type='withdraw_employee'))

    def get_today_records(self):
        return self.get_queryset().filter(created_at__date=timezone.now())

    def list(self, request):
        records = self.filter_queryset(self.get_queryset())

        return Response({
                'records': self.CashRecordSerializer(records, many=True).data,
                'total': records.calc_sum(),
                },
                 status=status.HTTP_200_OK)

    def create(self, request, serializer_class=CashRecordCreateExpenseSerializer):
        serializer = self.CashRecordCreateExpenseSerializer(data=request.data)
        if serializer.is_valid():
            cash_record = CashRecord.objects.create_rama_expense(
                amount=serializer.validated_data['amount'],
                note=serializer.validated_data['note'],
                initiator=request.user
                )

            records = self.get_today_records()

            return Response({
                'expense': self.CashRecordSerializer(cash_record).data,
                'records': self.CashRecordSerializer(records, many=True).data,
                'total': records.calc_sum(),
                'message': 'Успешно'
                },
                 status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        self.get_object().delete()
        records = self.get_today_records()
        return Response({
            'records': self.CashRecordSerializer(self.get_queryset(), many=True).data,
            'totals': records.calc_sum()
            },
            status=status.HTTP_200_OK)


# resaw
class ReSawViewSet(viewsets.ModelViewSet):

    class ReSawSerializer(serializers.ModelSerializer):
        lumber_in = serializers.ReadOnlyField(source='lumber_in.lumber.name')
        lumber_in_quantity = serializers.ReadOnlyField(source='lumber_in.quantity')
        lumber_in_wood_species = serializers.ReadOnlyField(source='lumber_in.lumber.wood_species')

        lumber_out = serializers.ReadOnlyField(source='lumber_out.lumber.name')
        lumber_out_quantity = serializers.ReadOnlyField(source='lumber_out.quantity')
        lumber_out_wood_species = serializers.ReadOnlyField(source='lumber_out.lumber.wood_species')

        who = serializers.ReadOnlyField(source='initiator.account.nickname')

        class Meta:
            model = ReSaw
            fields = ['id', 'created_at', 'lumber_in', 'lumber_in_quantity', 'lumber_out', 
                'lumber_out_quantity', 'lumber_in_wood_species', 'who',
                'lumber_out_wood_species']


    class CreateReSawSerializer(serializers.Serializer):
        lumber_in = serializers.PrimaryKeyRelatedField(queryset=Lumber.objects.all())
        lumber_in_quantity = serializers.IntegerField()

        lumber_out = serializers.PrimaryKeyRelatedField(queryset=Lumber.objects.all())
        lumber_out_quantity = serializers.IntegerField()

        rama = serializers.PrimaryKeyRelatedField(queryset=Rama.objects.all())

        class Meta:
            model = ReSaw
            fields = ['id', 'created_at', 'lumber_in', 'lumber_in_quantity', 'lumber_out', 
                'lumber_out_quantity', 'rama']


    class OnlyCapoCanCreatePermissions(permissions.BasePermission):
        def has_permission(self, request, view):
            if request.method == 'POST' or request.method == 'DELETE':
                return request.user.account.is_boss or request.user.account.is_capo

            return False

        def has_object_permission(self, request, view, obj):
            if request.method == 'DELETE':
                return request.user.account.is_boss or request.user.account.is_capo

            return False

    permission_classes = [IsAuthenticated, OnlyCapoCanCreatePermissions]
    queryset = ReSaw.objects.all()
    serializer_class = ReSawSerializer

    # def get_queryset(self):
    #     return ReSaw.objects.filter(rama=self.request.user.account.rama)

    def create(self, request, serializer_class=CreateReSawSerializer):
        serializer = self.CreateReSawSerializer(data=request.data)
        if serializer.is_valid():
            resaw = ReSaw.objects.create_resaw(
                resaw_lumber_in={'lumber': serializer.validated_data['lumber_in'],
                    'quantity': serializer.validated_data['lumber_in_quantity']},
                resaw_lumber_out={'lumber': serializer.validated_data['lumber_out'],
                    'quantity': serializer.validated_data['lumber_out_quantity']},
                rama=serializer.validated_data['rama'],
                initiator=request.user
                )
            return Response({
                'created': self.ReSawSerializer(resaw).data,
                'resaws': self.ReSawSerializer(
                    self.get_queryset().filter(rama=request.user.account.rama),
                     many=True).data,
                'message': 'Успешно'
                },
                 status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        self.get_object().delete()
        return Response({
            'resaws': self.ReSawSerializer(
                    self.get_queryset().filter(rama=request.user.account.rama), many=True).data,
            },
            status=status.HTTP_200_OK)



class IncomeTimberViewSet(viewsets.ModelViewSet):

    class ReadTimberSerializer(serializers.ModelSerializer):
        timber = serializers.ReadOnlyField(source='pk')
        wood_species = ChoiceField(read_only=True, choices=Timber.SPECIES)
        quantity = serializers.IntegerField(default=0, read_only=True)

        class Meta:
            model = Timber
            fields = ['id', 'wood_species', 'diameter', 'volume', 'timber', 'quantity']


    class IncomeTimberSerializer(serializers.ModelSerializer):

        class RawTimberRecordSerializer(serializers.Serializer):
            timber = serializers.PrimaryKeyRelatedField(queryset=Timber.objects.all())
            quantity = serializers.IntegerField()

        timber_records = RawTimberRecordSerializer(many=True, read_only=True)

        class Meta:
            model = IncomeTimber
            fields = ['pk', 'quantity', 'volume', 'rama', 'created_at', 'timber_records']


    class CreateIncomeTimberSerializer(serializers.Serializer):

        class RawTimberRecordSerializer(serializers.Serializer):
            timber = serializers.PrimaryKeyRelatedField(queryset=Timber.objects.all())
            quantity = serializers.IntegerField()

        raw_timber_records = RawTimberRecordSerializer(many=True)
        note = serializers.CharField(required=False)


    class ReadIncomeTimberSerializer(serializers.ModelSerializer):

        class TimberRecordSerializer(serializers.ModelSerializer):
            timber = serializers.StringRelatedField()
            wood_species = ChoiceField(source='timber.wood_species', read_only=True,
             choices=Timber.SPECIES)
            total_volume = serializers.ReadOnlyField(source='volume')
            diameter = serializers.ReadOnlyField(source='timber.diameter')

            class Meta:
                model = TimberRecord
                fields = ['timber', 'quantity', 'volume', 'wood_species', 'total_volume', 'diameter']

        who = serializers.ReadOnlyField(source='initiator.account.nickname')
        timber_records = TimberRecordSerializer(many=True)

        class Meta:
            model = IncomeTimber
            fields = ['id', 'created_at', 'who', 'quantity', 'volume', 'note', 'timber_records']


    class OnlyManagerCanCreateBossDeletePermissions(permissions.BasePermission):
        def has_permission(self, request, view):
            if request.method in permissions.SAFE_METHODS:
                return request.user.account.is_manager or request.user.account.is_boss

            if request.method == 'POST':
                return request.user.account.is_manager

            if request.method == 'DELETE':
                return request.user.account.is_boss

            return False

        def has_object_permission(self, request, view, obj):
            if request.method == 'DELETE':
                return request.user.account.is_boss

            return False

    queryset = IncomeTimber.objects.all()
    serializer_class = IncomeTimberSerializer
    permission_classes = [IsAuthenticated, OnlyManagerCanCreateBossDeletePermissions]

    @action(detail=False, methods=['get'])
    def init_data(self, request, pk=None):
        return Response({
            'timbers': self.ReadTimberSerializer(
                Timber.objects.all().order_by('-wood_species', 'diameter'), many=True).data,
            }, status=status.HTTP_200_OK)

    def create(self, request, serializer_class=CreateIncomeTimberSerializer):
        serializer = self.CreateIncomeTimberSerializer(data=request.data)
        if serializer.is_valid():
            income_timber = IncomeTimber.objects.create_income_timber(
                raw_timber_records=serializer.validated_data['raw_timber_records'],
                note=serializer.validated_data.get('note'),
                initiator=request.user,
                rama=request.user.account.rama
                )
            
            return Response({
                'income_timber': self.ReadIncomeTimberSerializer(income_timber).data,
                'message': 'Успешно'
                },
                 status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        self.get_object().delete()
        return Response({
            'income_timbers': self.ReadIncomeTimberSerializer(
                    self.get_queryset().filter(rama=request.user.account.rama), many=True).data,
            },
            status=status.HTTP_200_OK)


# payout to manager
class PayoutToManagerView(viewsets.ModelViewSet):

    class CreateManagerPayoutSerializer(serializers.Serializer):
        rama = serializers.PrimaryKeyRelatedField(queryset=Rama.objects.all())
        amount = serializers.IntegerField()


    class CashRecordWithTypeSerializer(serializers.ModelSerializer):
        record_type = ChoiceField(read_only=True, choices=CashRecord.RECORD_TYPES)
        who = serializers.ReadOnlyField(source='initiator.account.nickname')

        class Meta:
            model = CashRecord
            fields = ['created_at', 'amount', 'note', 'record_type', 'who', 'id']


    class ExpensesFilter(filters.FilterSet):
        created_at = filters.DateFromToRangeFilter()

        class Meta:
            model = CashRecord
            fields = '__all__'


    class BossOrCapoPermission(permissions.BasePermission):
        def has_permission(self, request, view):
            if request.method == 'POST' or request.method == 'DELETE':
                return request.user.account.is_boss or request.user.account.is_capo

        def has_object_permission(self, request, view, obj):
            if request.method == 'DELETE':
                return request.user.account.is_boss
            return False

    queryset = CashRecord.objects.all()
    serializer_class = CashRecordWithTypeSerializer
    filter_class = ExpensesFilter
    permission_classes = [IsAuthenticated, BossOrCapoPermission]

    def destroy(self, request, pk=None):
        rama = self.get_object().rama
        self.get_object().delete()
        records = CashRecord.objects.filter(rama=rama) \
                        .filter(Q(record_type='withdraw_cash_from_manager') |
                                Q(record_type='income_timber')) \
                        .order_by('-created_at')
        return Response({
            'cash_records': self.CashRecordWithTypeSerializer(records, many=True).data,
            'manager_balance': records.calc_manager_balance()
            },
            status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], serializer_class=CreateManagerPayoutSerializer)
    def payout_to_manager(self, request, pk=None):
        serializer = self.CreateManagerPayoutSerializer(data=request.data)
        if serializer.is_valid():
            rama = serializer.validated_data['rama']
            manager = Account.objects.filter(rama=rama, is_manager=True).first()

            CashRecord.objects.create_withdraw_cash_from_manager(
                manager_account=manager,
                initiator=request.user,
                amount=serializer.validated_data['amount']
            )

            cash_records = CashRecord.objects.filter(rama=rama) \
                        .filter(Q(record_type='withdraw_cash_from_manager') |
                                Q(record_type='income_timber')) \
                        .order_by('-created_at')

            return Response({
                'cash_records': self.CashRecordWithTypeSerializer(cash_records, many=True).data,
                'manager_balance': cash_records.calc_manager_balance()
                },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)