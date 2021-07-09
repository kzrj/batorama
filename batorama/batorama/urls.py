# -*- coding: utf-8 -*-
import os
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings

from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from apis import manager_api, ramshik_api, kladman_api, common_api

# router = routers.DefaultRouter()
# router.register(r'shifts', ShiftViewSet, basename='shifts')
# router.register(r'manager/ramshik_payments', RamshikiPaymentViewSet, basename='ramshik_payments')

urlpatterns = [
    path('admin/', admin.site.urls),
    # url(r'^api/', include(router.urls)),
    url(r'^api/init_data/$', ramshik_api.InitTestDataView.as_view()),
    url(r'^api/jwt/api-token-auth/', obtain_jwt_token),
    url(r'^api/jwt/api-token-refresh/', refresh_jwt_token),
    url(r'^api/jwt/api-token-verify/', verify_jwt_token),

    # common read api
    path('api/common/stock/', common_api.LumberStockListView.as_view()),
    path('api/common/shifts/', common_api.ShiftListView.as_view()),
    path('api/common/sales/', common_api.SalesListView.as_view()),
    path('api/common/cash/', common_api.CashRecordsListView.as_view()),

    # manager api
    path('api/manager/ramshik_payments/init_data/', manager_api.RamshikiPaymentViewSet.as_view({'get': 'init_data'})),
    path('api/manager/ramshik_payments/ramshik_payout/', manager_api.RamshikiPaymentViewSet.as_view({'post': 'ramshik_payout'})),
    path('api/manager/shift_list/', manager_api.ShiftListView.as_view()),
    path('api/manager/stock/', manager_api.LumberStockListView.as_view()),
    path('api/manager/sale_list/', manager_api.SaleListView.as_view()),
    # path('api/manager/total_sales/', SaleListView.as_view({'get': 'total_sales'})),
    path('api/manager/stock/set_price/', manager_api.SetLumberMarketPriceView.as_view()),
    path('api/manager/rawstock/timber/create_income/', manager_api.IncomeTimberViewSet.as_view({'post': 'create'})),
    path('api/manager/rawstock/timber/create_income/init_data/', manager_api.IncomeTimberViewSet.as_view({'get': 'init_data'})),
    path('api/manager/quota/overview/', manager_api.QuotasPageView.as_view()),

    # ramshik api
    path('api/ramshik/shifts/create/init_data/', ramshik_api.ShiftViewSet.as_view({'get': 'shift_create_data'})),
    path('api/ramshik/shifts/create/', ramshik_api.ShiftViewSet.as_view({'post': 'create'})),
    path('api/ramshik/shifts/list/', ramshik_api.ShiftViewSet.as_view({'get': 'list'})),
    path('api/ramshik/payouts/', ramshik_api.RamshikPayoutViewSet.as_view({'get': 'get_data'})),

    # kladman api
    path('api/kladman/sales/create/init_data/', kladman_api.SaleView.as_view({'get': 'sale_create_data'})),
    path('api/kladman/sales/create/', kladman_api.SaleView.as_view({'post': 'create'})),
    path('api/kladman/sales/calc_data/', kladman_api.SaleView.as_view({'get': 'sale_calc_data'})),
    path('api/kladman/sales/<int:pk>/', kladman_api.SaleView.as_view({'delete': 'destroy'})),
    path('api/kladman/cash_records/create_expense/', kladman_api.CashRecordsView.as_view({'post': 'create_expense'})),
    path('api/kladman/cash_records/list/', kladman_api.CashRecordsView.as_view({'get': 'list'})),
    path('api/kladman/daily_report/', kladman_api.DailyReport.as_view()),
    path('api/kladman/resaws/create/', kladman_api.ReSawViewSet.as_view({'post': 'create'})),
    path('api/kladman/resaws/list/', kladman_api.ReSawViewSet.as_view({'get': 'list'})),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
