from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,    # 獲取 access token 和 refresh token
    TokenRefreshView,       # 用 refresh token 換取新的 access token
    TokenVerifyView,         # 驗證 token 是否有效
    TokenBlacklistView,
)
from pet_booking.users.views import *
from pet_booking.customers.views import *
from pet_booking.stores.views import *
from pet_booking.services.views import *
from pet_booking.reservations.views import *

router = DefaultRouter(trailing_slash=False)


urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
