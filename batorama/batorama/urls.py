# -*- coding: utf-8 -*-
import os
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings

from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from apis.manager_api import ( RamshikiPaymentViewSet, ShiftListView, LumberStockListView,
 SaleListView, SetLumberMarketPriceView)
from apis.ramshik_api import ShiftViewSet, InitTestDataView, RamshikPayoutViewSet
from apis.kladman_api import SaleView, CashRecordsView, DailyReport

# router = routers.DefaultRouter()
# router.register(r'shifts', ShiftViewSet, basename='shifts')
# router.register(r'manager/ramshik_payments', RamshikiPaymentViewSet, basename='ramshik_payments')

urlpatterns = [
    path('admin/', admin.site.urls),
    # url(r'^api/', include(router.urls)),
    url(r'^api/init_data/$', InitTestDataView.as_view()),
    url(r'^api/jwt/api-token-auth/', obtain_jwt_token),
    url(r'^api/jwt/api-token-refresh/', refresh_jwt_token),
    url(r'^api/jwt/api-token-verify/', verify_jwt_token),

    # manager api
    path('api/manager/ramshik_payments/init_data/', RamshikiPaymentViewSet.as_view({'get': 'init_data'})),
    path('api/manager/ramshik_payments/ramshik_payout/', RamshikiPaymentViewSet.as_view({'post': 'ramshik_payout'})),
    path('api/manager/shift_list/', ShiftListView.as_view()),
    path('api/manager/stock/', LumberStockListView.as_view()),
    path('api/manager/sale_list/', SaleListView.as_view()),
    # path('api/manager/total_sales/', SaleListView.as_view({'get': 'total_sales'})),
    path('api/manager/stock/set_price/', SetLumberMarketPriceView.as_view()),

    # ramshik api
    path('api/ramshik/shifts/create/init_data/', ShiftViewSet.as_view({'get': 'shift_create_data'})),
    path('api/ramshik/shifts/create/', ShiftViewSet.as_view({'post': 'create'})),
    path('api/ramshik/shifts/list/', ShiftViewSet.as_view({'get': 'list'})),
    path('api/ramshik/payouts/', RamshikPayoutViewSet.as_view({'get': 'get_data'})),

    # kladman api
    path('api/kladman/sales/create/init_data/', SaleView.as_view({'get': 'sale_create_data'})),
    path('api/kladman/sales/create/', SaleView.as_view({'post': 'create'})),
    path('api/kladman/sales/calc_data/', SaleView.as_view({'get': 'sale_calc_data'})),
    path('api/kladman/sales/<int:pk>/', SaleView.as_view({'delete': 'destroy'})),
    path('api/kladman/cash_records/create_expense/', CashRecordsView.as_view({'post': 'create_expense'})),
    path('api/kladman/cash_records/list/', CashRecordsView.as_view({'get': 'list'})),
    path('api/kladman/daily_report/', DailyReport.as_view()),


]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
