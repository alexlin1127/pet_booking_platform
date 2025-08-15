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
from pet_booking.reservations.views.create_reservations import *
from pet_booking.reservations.views.manage_grooming_reservations import *
from pet_booking.reservations.views.manage_boarding_reservations import *
from pet_booking.reservations.views.manage_history_reservations import *
from pet_booking.reservations.views.manage_risk_reservations import (
    RiskGroomingViewSet,
    RiskBoardingViewSet,
    RiskStoreNoteUpdateViewSet
)

router = DefaultRouter(trailing_slash=False)

# Customers, admin, stores and pets 
router.register(r'users', UserViewSet, basename='users')
router.register(r'customer/profiles', CustomersProfileViewSet, basename='customer-profile')
router.register(r'customer/likestores', LikeStoreViewSet, basename='likestores')
router.register(r'customer/pets', PetViewSet, basename='pets')
router.register(r'admin/stores', StoreAdminViewSet, basename='admin-stores')
router.register(r'store/profile', StoreProfileViewSet, basename='store-profile')

# Post
router.register(r'store/posts', StorePostViewSet, basename='store-posts')
router.register(r'admin/posts', AdminPostViewSet, basename='admin-posts')
router.register(r'customer/store', CustomerStoreViewSet, basename='customer-store')
router.register(r'customer/post', CustomerPostViewSet, basename='customer-post')

router.register(r'store/boarding_services', BoardingServiceViewSet, basename='boarding_services')
router.register(r'store/grooming_services', GroomingServiceViewSet, basename='grooming_services')
router.register(r'customer/boarding_services', CustomerBoardingViewSet, basename='customer_boarding')
router.register(r'customer/grooming_services', CustomerGroomingViewset, basename='customer_grooming')
router.register(r'store/images', StoreImageViewSet, basename='store-images')

# Reservation related endpoints
router.register(r'store-info', StoreInfoViewSet, basename='store-info')
router.register(r'pet-info', PetInfoViewSet, basename='pet-info')
router.register(r'grooming/calculation', GroomingCalculationViewSet, basename='grooming-calculation')
router.register(r'grooming/reservation', GroomingReservationViewSet, basename='grooming-reservation')
router.register(r'boarding/room', BoardingRoomInfoViewSet, basename='boarding-room-info')
router.register(r'boarding/calculation', BoardingCalculationViewSet, basename='boarding-calculation')
router.register(r'boarding/reservation', BoardingReservationViewSet, basename='boarding-reservation')

# Reservation management endpoints
router.register(r'reservations/grooming/today', GroomingReservationInfoViewSet, basename='today-reservations')
router.register(r'reservations/grooming/notes', StoreNoteUpdateViewSet, basename='reservation-notes')
router.register(r'reservations/grooming/actions', GroomingReservationManagementViewSet, basename='reservation-actions')

# Reservation listing and details endpoints
router.register(r'reservations/grooming/pending', PendingReservationViewSet, basename='pending-reservations')
router.register(r'reservations/grooming/upcoming', UpcomingReservationViewSet, basename='upcoming-reservations')
router.register(r'reservations/grooming/overview', AllReservationsViewSet, basename='reservations-overview')
router.register(r'reservations/grooming/details', GroomingReservationDetailsViewSet, basename='grooming-details')

# Boarding room availability endpoint
router.register(r'reservations/boarding/availability', BoardingRoomAvailabilityViewSet, basename='boarding-availability')
router.register(r'reservations/boarding/notes', BoardingStoreNoteUpdateViewSet, basename='boarding-notes')
router.register(r'reservations/boarding/actions', BoardingReservationManagementViewSet, basename='boarding-actions')
router.register(r'reservations/boarding/overview', BoardingAllReservationsViewSet, basename='boarding-overview')
router.register(r'reservations/boarding/details', BoardingReservationDetailsViewSet, basename='boarding-details')
router.register(r'reservations/boarding/pending', BoardingPendingReservationViewSet, basename='boarding-pending')
router.register(r'reservations/boarding/upcoming', BoardingUpcomingReservationViewSet, basename='boarding-upcoming')
router.register(r'reservations/boarding/pending/detail', BoardingPendingReservationDetailViewSet, basename='boarding-pending-detail')

# History endpoints
router.register(r'reservations/grooming/history', GroomingHistoryViewSet, basename='grooming-history')
router.register(r'reservations/boarding/history', BoardingHistoryViewSet, basename='boarding-history')

# Customer observation endpoints
router.register(r'reservations/customer-observation', CustomerObservationViewSet, basename='customer-observation')

# Risk management endpoints (blacklist customers)
router.register(r'reservations/risk/grooming', RiskGroomingViewSet, basename='risk-grooming')
router.register(r'reservations/risk/boarding', RiskBoardingViewSet, basename='risk-boarding')
router.register(r'reservations/risk/notes', RiskStoreNoteUpdateViewSet, basename='risk-notes')
router.register(r'reservations/details', ReservationDetailsViewSet, basename='reservation-details')

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify', TokenVerifyView.as_view(), name='token_verify'),
    path('api/token/blacklist', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('api/register_send_code', RegisterSendCodeAPIView.as_view(), name='register_send_code'),
    path('api/register_confirm_code', RegisterConfirmCodeAPIView.as_view(), name='register_confirm_code'),
    path('api/store/register_send_code', StoreRegisterSendCodeAPIView.as_view()),
    path('api/store/register_confirm_code', StoreRegisterConfirmCodeAPIView.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
