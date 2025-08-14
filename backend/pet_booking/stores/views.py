import random
from django.core.mail import send_mail
from django.core.cache import cache
from django.contrib.auth.hashers import make_password
from rest_framework import viewsets
from rest_framework import status
from rest_framework.views import APIView
from django.db import models
from .models import Store, Post, StoreImage
from .serializers import StoreRegisterSendCodeSerializer, StoreRegisterConfirmCodeSerializer, StoreSerializer, PostSerializer, StoreImageSerializer, StoreListSerializer, StoreDetailSerializer
from pet_booking.users.models import User, UserRole
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
# Create your views here.

def generate_code(length=6):
    return ''.join(random.choices('0123456789', k=length))

class StoreRegisterSendCodeAPIView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = StoreRegisterSendCodeSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            # 查重
            if User.objects.filter(username=data['username']).exists():
                return Response({'msg': '該帳號已註冊'}, status=400)
            if User.objects.filter(email=data['email']).exists():
                return Response({'msg': '該 email 已註冊'}, status=400)
            if Store.objects.filter(phone=data['phone']).exists():
                return Response({'msg': '該電話已註冊'}, status=400)

            code = generate_code()
            hashed_pwd = make_password(data['password'])
            cache.set(
                f"store_register_{data['email']}",
                {
                    'username': data['username'],
                    'password': hashed_pwd,
                    'email': data['email'],
                    'phone': data['phone'],
                    'code': code,
                },
                timeout=60
            )
            send_mail(
                '您的店家註冊驗證碼',
                f'您的店家註冊驗證碼是：{code}',
                None,
                [data['email']]
            )
            return Response({'msg': '驗證碼已寄出'}, status=200)
        return Response(serializer.errors, status=400)

class StoreRegisterConfirmCodeAPIView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = StoreRegisterConfirmCodeSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            code = serializer.validated_data['code']
            cache_data = cache.get(f"store_register_{email}")

            if not cache_data:
                return Response({'msg': '驗證逾時'}, status=400)
            if cache_data['code'] != code:
                return Response({'msg': '驗證碼錯誤'}, status=400)

            # 雙重查重
            if User.objects.filter(username=cache_data['username']).exists():
                return Response({'msg': '該帳號已註冊'}, status=400)
            if User.objects.filter(email=email).exists():
                return Response({'msg': '該 email 已註冊'}, status=400)
            if Store.objects.filter(phone=cache_data['phone']).exists():
                return Response({'msg': '該電話已註冊'}, status=400)

            # 創建 User
            user = User.objects.create(
                username=cache_data['username'],
                password=cache_data['password'],
                email=email,
                role=UserRole.STORE,
                is_store_owner=True,
            )
            # 創建 Store
            store_name = request.data.get('store_name', '')
            owner_name = request.data.get('owner_name', '')
            address =  request.data.get('address', '')
            Store.objects.create(
                user_id=user,
                store_name=store_name,
                owner_name=owner_name,
                address=address,
                email=email,
                phone=cache_data['phone'],
                status='pending',   # 或你要的預設值
            )
            cache.delete(f"store_register_{email}")
            return Response({'msg': '註冊成功'}, status=201)
        return Response(serializer.errors, status=400)

# -------------------------------------------------------------------------------------------------

class StoreFilter(django_filters.FilterSet):
    created_at_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_at_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    class Meta:
        model = Store
        fields = ['status', 'created_at_after', 'created_at_before']

class PostFilter(django_filters.FilterSet):
    created_at_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_at_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    class Meta:
        model = Post
        fields = ['status', 'created_at_after', 'created_at_before']

# 店家詳情
class StoreProfileViewSet(viewsets.ModelViewSet):
    serializer_class = StoreSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    def get_queryset(self):
        return Store.objects.filter(user_id=self.request.user)

    def get_object(self):
        # 只允許編輯自己的 store
        return Store.objects.get(user_id=self.request.user)

    def perform_create(self, serializer):
        if not self.request.user.is_store_owner:
            raise PermissionDenied("只有店家帳號才能新增店家資訊。")
        if Store.objects.filter(user_id=self.request.user).exists():
            from rest_framework.exceptions import ValidationError
            raise ValidationError("每個使用者只能新增一筆店家資訊")
        serializer.save(user_id=self.request.user)
        
# 店家文章
class StorePostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(store__user_id=self.request.user)

    def perform_create(self, serializer):
        store = Store.objects.get(user_id=self.request.user)
        serializer.save(store=store)

    def perform_update(self, serializer):
        store = Store.objects.get(user_id=self.request.user)
        serializer.save(store=store)

    def perform_destroy(self, instance):
        if instance.store.user_id == self.request.user:
            instance.delete()

# 店家圖片
class StoreImageViewSet(viewsets.ModelViewSet):
    serializer_class = StoreImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return StoreImage.objects.filter(store__user_id=self.request.user)

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

# class StorePagination(PageNumberPagination):
#     page_size = 5
#     page_size_query_param = 'page_size'
#     max_page_size = 50

# 管理者店家頁
class StoreAdminViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all().order_by('-created_at')
    filter_backends = [DjangoFilterBackend]
    filterset_class= StoreFilter
    # pagination_class = StorePagination
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return StoreListSerializer
        elif self.action == 'retrieve':
            return StoreDetailSerializer
        return StoreDetailSerializer  # Default serializer for other actions


    @action(detail=False, methods=['get'])
    def statistics(self, request):
        pending_store_count = Store.objects.filter(status__in=['pending', 'repending']).count()
        pending_post_count = Post.objects.filter(status__in=['pending', 'repending']).count()
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
    filterset_class= PostFilter
    # pagination_class = StorePagination
    permission_classes = [IsAuthenticated]


# 使用者
# 使用者-店家清單

class CustomerStoreFilter(django_filters.FilterSet):
    county = django_filters.CharFilter(method='filter_county')
    district = django_filters.CharFilter(method='filter_district')

    class Meta:
        model = Store
        fields = ['service_item', 'county', 'district']
        filter_overrides = {
            models.JSONField: {
                'filter_class': django_filters.CharFilter,
            },
        }

    def filter_county(self, queryset, name, value):
        return queryset.filter(address__county=value)

    def filter_district(self, queryset, name, value):
        return queryset.filter(address__district=value)


# class CustomerStorePagination(PageNumberPagination):
#     page_size = 9
#     page_size_query_param = 'page_size'
#     max_page_size = 50

class CustomerStoreViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    permission_classes = []
    serializer_class = StoreListSerializer
    # pagination_class = CustomerStorePagination
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
    

# class CustomerPostPagination(PageNumberPagination):
#     page_size = 10
#     page_size_query_param = 'page_size'
#     max_page_size = 50

class CustomerPostViewSet(viewsets.ModelViewSet):
    permission_classes = []
    http_method_names = ['get']
    serializer_class = PostSerializer
    # pagination_class = CustomerPostPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = CustomerPostFilter
    queryset = Post.objects.filter(status='confirmed').order_by('-created_at')



