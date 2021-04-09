# -*- coding: utf-8 -*-
import os
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings

from rest_framework import routers

from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from stock.views import ShiftViewSet, InitTestDataView

router = routers.DefaultRouter()
router.register(r'shifts', ShiftViewSet, basename='shifts')

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'^api/init_data/$', InitTestDataView.as_view()),
    url(r'^api/jwt/api-token-auth/', obtain_jwt_token),
    url(r'^api/jwt/api-token-refresh/', refresh_jwt_token),
    url(r'^api/jwt/api-token-verify/', verify_jwt_token),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)