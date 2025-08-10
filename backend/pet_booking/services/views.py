from rest_framework import viewsets
from .models import BoardingService, GroomingService, BoardingServicePricing, GroomingServicePricing
from .serializers import BoardingServiceSerializer, GroomingServiceSerializer, BoardingServicePricingSerializer, GroomingServicePricingSerializer
from rest_framework.permissions import IsAuthenticated
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

# Create your views here.
#店家服務
class ServicePagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 10

class BoardingServiceViewSet(viewsets.ModelViewSet):
    serializer_class = BoardingServiceSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = ServicePagination

    def get_queryset(self):
        return BoardingService.objects.filter(store_id__user_id=self.request.user)

class BoardingServicePricingViewset(viewsets.ModelViewSet):
    queryset = BoardingServicePricing.objects.all()
    serializer_class = BoardingServicePricingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return GroomingService.objects.filter(store_id__user_id=self.request.user)


class GroomingServiceViewSet(viewsets.ModelViewSet):
    serializer_class = GroomingServiceSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = ServicePagination

    def get_queryset(self):
        return GroomingService.objects.filter(store_id__user_id=self.request.user)

class GroomingServicePricingViewset(viewsets.ModelViewSet):
    serializer_class = GroomingServicePricingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return GroomingServicePricing.objects.filter(store_id__user_id=self.request.user)

# 使用者-店家服務
class CustomerBoardingViewSet(viewsets.ModelViewSet):
    serializer_class = BoardingServiceSerializer
    queryset = BoardingService.objects.all()
    pagination_class = ServicePagination

class CustomerGroomingViewset(viewsets.ModelViewSet):
    serializer_class = GroomingServiceSerializer
    queryset = GroomingService.objects.all()
    pagination_class = ServicePagination
