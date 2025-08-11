# apps/customers/views.py
from rest_framework import viewsets, status
from rest_framework.permissions import BasePermission, AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
# from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import CustomersProfile, LikeStore, Pet
from .serializers import CustomersProfileSerializer, LikeStoreSerializer, PetSerializer
from pet_booking.users.models import User, UserRole
# from pet_booking.users.serializers import UserSerializer

# Create your views here.
class IsAdminOrOwner(BasePermission):
    """
    Admin 可存取全部資料，普通會員只能存取自己的資料
    """
    def has_object_permission(self, request, view, obj):
        # 管理員可以操作所有物件
        if request.user.is_authenticated and request.user.role == UserRole.ADMIN:
            return True
        # 物件必須有 user_id 欄位（ForeignKey 到 User）and # 操作的user id 要等於 發出request的 user id 
        return hasattr(obj, "user_id") and obj.user_id == request.user

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10              # 每頁顯示 10 筆
    page_size_query_param = 'page_size'  # 可用 URL ?page_size=20 動態調整
    max_page_size = 50         # 最大每頁顯示數
    
class BaseOwnerViewSet(viewsets.ModelViewSet):
    """
    Base ViewSet：
      - Admin 全部可見
      - 普通使用者只能看到/操作自己的資料
      - 建立時自動綁定登入用戶
      - 僅 Admin 可用 user_id 過濾
    """
    permission_classes = [IsAuthenticated, IsAdminOrOwner]
    filter_backends = [DjangoFilterBackend]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.role == UserRole.ADMIN:
            return self.queryset.all().order_by('-id')
        return self.queryset.filter(user_id=user).order_by('-id')

    def perform_create(self, serializer):
        # 強制綁定當前登入使用者
        serializer.save(user_id=self.request.user)

class CustomersProfileFilter(filters.FilterSet):
    class Meta:
        model = CustomersProfile
        fields = []  # 先不開任何欄位

    @property
    def filters(self):
        # 取得原本所有欄位型別
        filters_dict = super().filters.copy()
        # 根據 request.user 權限動態調整
        user = getattr(getattr(self, 'request', None), 'user', None)
        if user and user.is_authenticated and user.role == UserRole.ADMIN:
            # 只有 admin 能用 user_id 過濾
            filters_dict['user_id'] = filters.ModelChoiceFilter(queryset=User.objects.all())
        return filters_dict

class CustomersProfileViewSet(BaseOwnerViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = CustomersProfile.objects.all()
    serializer_class = CustomersProfileSerializer
    filterset_class = CustomersProfileFilter

    @action(detail=False, methods=['get', 'patch', 'delete'], url_path='me')
    def me(self, request):
        """
        GET    /customer/profiles/me/     取得自己的 CustomersProfile
        PATCH  /customer/profiles/me/     修改自己的 CustomersProfile
        DELETE /customer/profiles/me/     刪除自己的 CustomersProfile
        """
        try:
            profile = CustomersProfile.objects.get(user_id=request.user)
        except CustomersProfile.DoesNotExist:
            return Response({'detail': '沒有找到您的客戶資料'}, status=status.HTTP_404_NOT_FOUND)

        if request.method.lower() == 'get':
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        elif request.method.lower() == 'patch':
            serializer = self.get_serializer(profile, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        elif request.method.lower() == 'delete':
            profile.delete()
            return Response({"detail": "已刪除"}, status=status.HTTP_204_NO_CONTENT)

class LikeStoreFilter(filters.FilterSet):
    class Meta:
        model = LikeStore
        fields = []  # 先不開任何欄位

    @property
    def filters(self):
        # 取得原本所有欄位型別
        filters_dict = super().filters.copy()
        # 根據 request.user 權限動態調整
        user = getattr(getattr(self, 'request', None), 'user', None)
        if user and user.is_authenticated and user.role == UserRole.ADMIN:
            # 只有 admin 能用 user_id 過濾
            filters_dict['user_id'] = filters.ModelChoiceFilter(queryset=User.objects.all())
        return filters_dict

class LikeStoreViewSet(BaseOwnerViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = LikeStore.objects.all()
    serializer_class = LikeStoreSerializer
    filterset_class = LikeStoreFilter


    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        """
        GET /customer/likestores/me/ 取得自己的 LikeStore 列表
        """
        likestores = LikeStore.objects.filter(user_id=request.user).order_by('-id')
        serializer = self.get_serializer(likestores, many=True)
        return Response(serializer.data)

class PetFilter(filters.FilterSet):
    class Meta:
        model = Pet
        fields = []  # 先不開任何欄位

    @property
    def filters(self):
        # 取得原本所有欄位型別
        filters_dict = super().filters.copy()
        # 根據 request.user 權限動態調整
        user = getattr(getattr(self, 'request', None), 'user', None)
        if user and user.is_authenticated and user.role == UserRole.ADMIN:
            # 只有 admin 能用 user_id 過濾
            filters_dict['user_id'] = filters.ModelChoiceFilter(queryset=User.objects.all())
        return filters_dict

class PetViewSet(BaseOwnerViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    filterset_class = PetFilter


    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        """
        GET /customer/pets/me/ 取得自己的 Pet 列表
        """
        pets = Pet.objects.filter(user_id=request.user).order_by('-id')
        serializer = self.get_serializer(pets, many=True)
        return Response(serializer.data)