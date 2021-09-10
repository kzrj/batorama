# -*- coding: utf-8 -*-
import os
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings

from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from apis import manager_api, ramshik_api, kladman_api, common_api

urlpatterns = [
    path('admin/', admin.site.urls),
    # url(r'^api/', include(router.urls)),
    url(r'^api/init_data/$', ramshik_api.InitTestDataView.as_view()),
    url(r'^api/jwt/api-token-auth/', obtain_jwt_token),
    url(r'^api/jwt/api-token-refresh/', refresh_jwt_token),
    url(r'^api/jwt/api-token-verify/', verify_jwt_token),

    # common read api
    path('api/test/1c/', common_api.Test1CView.as_view()),

    # common read api
    path('api/common/stock/', common_api.LumberStockListView.as_view()),
    path('api/common/shifts/', common_api.ShiftListView.as_view()),
    path('api/common/sales/', common_api.SalesListView.as_view()),
    path('api/common/cash/', common_api.CashRecordsListView.as_view()),
    path('api/common/daily_report/', common_api.DailyReport.as_view()),
    path('api/common/sales/calc_data/', common_api.SaleCalcDataView.as_view()),
    path('api/common/resaw/', common_api.ResawListView.as_view()),
    path('api/common/income_timbers/', common_api.IncomeTimberListView.as_view()),
    path('api/common/quotas/', common_api.QuotasPageView.as_view()),

    # manager api
    path('api/manager/shifts/create/init_data/', manager_api.ShiftViewSet.as_view({'get': 'shift_create_data'})),
    path('api/manager/shifts/create/', manager_api.ShiftViewSet.as_view({'post': 'create'})),
    path('api/manager/shifts/<int:pk>/', manager_api.ShiftViewSet.as_view({'delete': 'destroy'})),

    path('api/manager/ramshik_payments/init_data/', manager_api.RamshikiPaymentViewSet.as_view({'get': 'init_data'})),
    path('api/manager/ramshik_payments/ramshik_payout/', manager_api.RamshikiPaymentViewSet.as_view({'post': 'ramshik_payout'})),
    path('api/manager/ramshiki/create/', manager_api.RamshikiPaymentViewSet.as_view({'post': 'create'})),
    path('api/manager/ramshiki/<int:pk>/', manager_api.RamshikiPaymentViewSet.as_view({'delete': 'destroy'})),

    path('api/manager/stock/set_price/', manager_api.SetLumberMarketPriceView.as_view()),

    path('api/manager/sales/create/init_data/', manager_api.SaleView.as_view({'get': 'sale_create_data'})),
    path('api/manager/sales/create/', manager_api.SaleView.as_view({'post': 'create'})),
    path('api/manager/sales/<int:pk>/', manager_api.SaleView.as_view({'delete': 'destroy'})),

    path('api/manager/cash_records/create_expense/', manager_api.CashRecordsView.as_view({'post': 'create'})),
    path('api/manager/cash_records/list/', manager_api.CashRecordsView.as_view({'get': 'list'})),
    path('api/manager/cash_records/<int:pk>/', manager_api.CashRecordsView.as_view({'delete': 'destroy'})),

    path('api/manager/resaws/create/', manager_api.ReSawViewSet.as_view({'post': 'create'})),
    path('api/manager/resaws/<int:pk>/', manager_api.ReSawViewSet.as_view({'delete': 'destroy'})),

    path('api/manager/rawstock/timber/create_income/', manager_api.IncomeTimberViewSet.as_view({'post': 'create'})),
    path('api/manager/rawstock/timber/create_income/init_data/', manager_api.IncomeTimberViewSet.as_view({'get': 'init_data'})),
    path('api/manager/rawstock/timber/income_timbers/<int:pk>/', manager_api.IncomeTimberViewSet.as_view({'delete': 'destroy'})),

    # boss, capo
    path('api/boss_capo/cash_records/payout_to_manager/', 
        manager_api.PayoutToManagerView.as_view({'post': 'payout_to_manager'})),
    path('api/boss_capo/cash_records/<int:pk>/', 
        manager_api.PayoutToManagerView.as_view({'delete': 'destroy'})),

    # ramshik api
    path('api/ramshik/shifts/list/', ramshik_api.ShiftListView.as_view()),
    path('api/ramshik/payouts/', ramshik_api.RamshikPayoutView.as_view()),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
