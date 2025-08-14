from rest_framework import viewsets
from .models import BoardingService, GroomingService
from pet_booking.stores.models import Store
from .serializers import BoardingServiceSerializer, GroomingServiceSerializer
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
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    serializer_class = BoardingServiceSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = ServicePagination

    def get_queryset(self):
        return BoardingService.objects.filter(store_id__user_id=self.request.user)

    def perform_create(self, serializer):
        store = Store.objects.get(user_id=self.request.user)
        serializer.save(store_id=store)


class GroomingServiceViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    serializer_class = GroomingServiceSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = ServicePagination

    def get_queryset(self):
        return GroomingService.objects.filter(store_id__user_id=self.request.user)
    
    def perform_create(self, serializer):
        store = Store.objects.get(user_id=self.request.user)
        serializer.save(store_id=store)



# 使用者-店家服務
class CustomerBoardingViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    permission_classes = []
    serializer_class = BoardingServiceSerializer
    queryset = BoardingService.objects.all()
    pagination_class = ServicePagination

class CustomerGroomingViewset(viewsets.ModelViewSet):
    http_method_names = ['get']
    permission_classes = []
    serializer_class = GroomingServiceSerializer
    queryset = GroomingService.objects.all()
    pagination_class = ServicePagination
