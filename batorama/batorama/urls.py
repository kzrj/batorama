# -*- coding: utf-8 -*-
import os
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings

from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from apis.manager_api import RamshikiPaymentViewSet, ShiftListView, LumberStockListView, SaleListView
from apis.ramshik_api import ShiftViewSet, InitTestDataView, RamshikPayoutViewSet
from apis.kladman_api import SaleList

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

    # ramshik api
    path('api/ramshik/shifts/create/init_data/', ShiftViewSet.as_view({'get': 'shift_create_data'})),
    path('api/ramshik/shifts/create/', ShiftViewSet.as_view({'post': 'create'})),
    path('api/ramshik/shifts/list/', ShiftViewSet.as_view({'get': 'list'})),
    path('api/ramshik/payouts/', RamshikPayoutViewSet.as_view({'get': 'get_data'})),

    # kladman api
    path('api/kladman/sales/create/init_data/', SaleList.as_view({'get': 'sale_create_data'})),
    path('api/kladman/sales/create/init_data_china/', SaleList.as_view({'get': 'sale_china_create_data'})),
    path('api/kladman/sales/create/', SaleList.as_view({'post': 'create'})),
    path('api/kladman/sales/create_schema1/', SaleList.as_view({'post': 'create_sale_schema1'})),


]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
