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
router.register(r'users', UserViewSet, basename='users')
router.register(r'customer/profiles', CustomersProfileViewSet, basename='customer-profile')
router.register(r'customer/likestores', LikeStoreViewSet, basename='likestores')
router.register(r'customer/pets', PetViewSet, basename='pets')
router.register(r'store/profile', StoreProfileViewSet, basename='store-profile')
router.register(r'admin/stores', StoreAdminViewSet, basename='admin-stores')
router.register(r'store/posts', StorePostViewSet, basename='store-posts')
router.register(r'admin/posts', AdminPostViewSet, basename='admin-posts')
router.register(r'store/images', StoreImageViewSet, basename='store-images')
router.register(r'store/boarding-services', BoardingServiceViewSet, basename='boarding-services')
router.register(r'store/grooming-services', GroomingServiceViewSet, basename='grooming-services')
router.register(r'store/boarding-pricings', BoardingServicePricingViewset, basename='boarding-pricings')
router.register(r'store/grooming-pricings', GroomingServicePricingViewset, basename='grooming-pricings')

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify', TokenVerifyView.as_view(), name='token_verify'),
    path('api/token/blacklist', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
