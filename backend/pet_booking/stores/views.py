from rest_framework import viewsets
from .models import Store, Post, StoreImage
from .serializers import StoreSerializer, PostSerializer, StoreImageSerializer, StoreListSerializer, StoreDetailSerializer
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response
# Create your views here.

class AdminFilter(django_filters.FilterSet):
    created_at_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_at_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    class Meta:
        model = Store
        fields = ['status', 'created_at_after', 'created_at_before']


# 店家詳情
class StoreProfileViewSet(viewsets.ModelViewSet):
    serializer_class = StoreSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Store.objects.filter(user_id=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user_id=self.request.user)

    def perform_destroy(self, instance):
        if instance.user_id == self.request.user:
            instance.delete()
    
# 店家文章
class StorePostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(store__user_id=self.request.user)

    def perform_create(self, serializer):
        store = Store.objects.get(user_id=self.request.user)
        serializer.save(store_id=store)

    def perform_update(self, serializer):
        store = Store.objects.get(user_id=self.request.user)
        serializer.save(store_id=store)

    def perform_destroy(self, instance):
        if instance.store.user_id == self.request.user:
            instance.delete()

# 店家圖片
class StoreImageViewSet(viewsets.ModelViewSet):
    serializer_class = StoreImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return StoreImage.objects.filter(user_id=self.request.user)

    def perform_create(self, serializer):
        store = Store.objects.get(user_id=self.request.user)
        serializer.save(store=store)


    def perform_update(self, serializer):
        store = Store.objects.get(user_id=self.request.user)
        serializer.save(store=store)

    def perform_destroy(self, instance):
        if instance.store.user_id == self.request.user:
            instance.delete()

# 管理者
# 分頁

class StorePagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 50

# 管理者店家頁
class StoreAdminViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all().order_by('-created_at')
    filter_backends = [DjangoFilterBackend]
    filterset_class= AdminFilter
    pagination_class = StorePagination
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return StoreListSerializer
        elif self.action == 'retrieve':
            return StoreDetailSerializer


    @action(detail=False, methods=['get'])
    def statistics(self, request):
        pending_store_count = Store.objects.filter(status='pending').count()
        pending_post_count = Post.objects.filter(status='pending').count()
        total_store_count = Store.objects.filter(status='confirmed').count()
        return Response({
            'pending_store_count': pending_store_count,
            'pending_post_count': pending_post_count,
            'total_store_count': total_store_count
        })

# 管理者文章
class AdminPostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('created_at')
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class= AdminFilter
    pagination_class = StorePagination
    permission_classes = [IsAuthenticated]


# 使用者
# 使用者-店家清單

class CustomerStoreFilter(django_filters.FilterSet):
    county = django_filters.CharFilter(method='filter_county')
    district = django_filters.CharFilter(method='filter_district')

    class Meta:
        model = Store
        fields = ['service_item', 'county', 'district']

    def filter_county(self, queryset, name, value):
        return queryset.filter(address__county=value)

    def filter_district(self, queryset, name, value):
        return queryset.filter(address__district=value)


class CustomerStorePagination(PageNumberPagination):
    page_size = 9
    page_size_query_param = 'page_size'
    max_page_size = 50

class CustomerStoreViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    serializer_class = StoreListSerializer
    pagination_class = CustomerStorePagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = CustomerStoreFilter
    queryset = Store.objects.filter(status='confirmed').order_by('-created_at')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return StoreSerializer
        return StoreListSerializer


# class GroomingStoreViewSet(viewsets.ModelViewSet):
#     http_method_names = ['get']
#     serializer_class = StoreListSerializer
#     pagination_class = CustomerStorePagination
#     filter_backends = [DjangoFilterBackend]
#     filterset_class = CustomerStoreFilter
#     queryset = Store.objects.filter(grooming_service=True, status='confirmed').order_by('-created_at')
    

# class BoardingStoreViewSet(viewsets.ModelViewSet):
#     http_method_names = ['get']
#     serializer_class = StoreListSerializer
#     pagination_class = CustomerStorePagination
#     filter_backends = [DjangoFilterBackend]
#     filterset_class = CustomerStoreFilter
#     queryset = Store.objects.filter(boarding_service=True, status='confirmed').order_by('-created_at')
    


# 使用者-貼文
class CustomerPostFilter(django_filters.FilterSet):
    class Meta:
        model = Post
        fields = ['type']
    

class CustomerPostPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50

class CustomerPostViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    serializer_class = PostSerializer
    pagination_class = CustomerPostPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = CustomerPostFilter
    queryset = Post.objects.filter(status='confirmed').order_by('-created_at')



