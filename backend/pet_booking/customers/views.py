# customers/views.py
import random
from django.core.cache import cache
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import BasePermission, AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
# from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import CustomersProfile, LikeStore, Pet
from .serializers import RegisterSendCodeSerializer, RegisterConfirmCodeSerializer, CustomersProfileSerializer, LikeStoreSerializer, PetSerializer
from pet_booking.users.models import User, UserRole
# from pet_booking.users.serializers import UserSerializer

# ----- Auth/註冊 驗證 API -----

def generate_code(length=6):
    return ''.join(random.choices('0123456789', k=length))

class RegisterSendCodeAPIView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = RegisterSendCodeSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            # 查 user、email 是否已存在
            if User.objects.filter(username=data['username']).exists():
                return Response({'msg': '該帳號已註冊'}, status=400)
            if User.objects.filter(email=data['email']).exists():
                return Response({'msg': '該 email 已註冊'}, status=400)
            if CustomersProfile.objects.filter(phone=data['phone']).exists():
                return Response({'msg': '該電話已註冊'}, status=400)
            
            code = generate_code()
            hashed_pwd = make_password(data['password'])
            cache.set(
                f"register_{data['email']}",
                {
                    'username': data['username'],
                    'password': hashed_pwd,
                    'phone': data['phone'],
                    'code': code,
                    'email': data['email'],  # 方便一致
                    'full_name': data['full_name'],
                },
                timeout=300
            )
            send_mail(
                '您的驗證碼',
                f'您的註冊驗證碼是：{code}',
                None,
                [data['email']]
            )
            return Response({'msg': '驗證碼已寄出'}, status=200)
        return Response(serializer.errors, status=400)

class RegisterConfirmCodeAPIView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = RegisterConfirmCodeSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            code = serializer.validated_data['code']
            cache_data = cache.get(f"register_{email}")

            if not cache_data:
                return Response({'msg': '驗證逾時'}, status=400)
            if cache_data['code'] != code:
                return Response({'msg': '驗證碼錯誤'}, status=400)

            # 雙重查重，避免 race condition
            if User.objects.filter(username=cache_data['username']).exists():
                return Response({'msg': '該帳號已註冊'}, status=400)
            if User.objects.filter(email=email).exists():
                return Response({'msg': '該 email 已註冊'}, status=400)
            if CustomersProfile.objects.filter(phone=cache_data['phone']).exists():
                return Response({'msg': '該電話已註冊'}, status=400)

            # 創建 User
            user = User.objects.create(
                username=cache_data['username'],
                password=cache_data['password'],
                email=email
            )
            # 創建 CustomersProfile
            CustomersProfile.objects.create(
                user_id=user,
                email=email,
                phone=cache_data['phone'],
                full_name=cache_data['full_name']
                # ...如有 gender, address 再補完整
            )
            cache.delete(f"register_{email}")
            return Response({'msg': '註冊成功'}, status=201)
        return Response(serializer.errors, status=400)
    

# ----- 以下是登入後會員管理 ViewSet -----
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

# class StandardResultsSetPagination(PageNumberPagination):
#     page_size = 10              # 每頁顯示 10 筆
#     page_size_query_param = 'page_size'  # 可用 URL ?page_size=20 動態調整
#     max_page_size = 50         # 最大每頁顯示數
    
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
    # pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.role == UserRole.ADMIN:
            return self.queryset.all().order_by('-id')
        return self.queryset.filter(user_id=user).order_by('-id')

    def perform_create(self, serializer):
        # 強制綁定當前登入使用者
        serializer.save(user_id=self.request.user)

# ------------------------filter------------------------------
class CustomersProfileFilter(filters.FilterSet):
    class Meta:
        model = CustomersProfile
        fields = []  # 預設沒有過濾欄位

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = getattr(self.request, 'user', None)
        if user and user.is_authenticated and user.role == UserRole.ADMIN:
            # 只有 admin 能用 user_id 過濾
            self.filters['user_id'] = filters.ModelChoiceFilter(queryset=User.objects.all())


class LikeStoreFilter(filters.FilterSet):
    class Meta:
        model = LikeStore
        fields = []  # 預設沒有過濾欄位

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = getattr(self.request, 'user', None)
        if user and user.is_authenticated and user.role == UserRole.ADMIN:
            self.filters['user_id'] = filters.ModelChoiceFilter(queryset=User.objects.all())


class PetFilter(filters.FilterSet):
    class Meta:
        model = Pet
        fields = []  # 預設沒有過濾欄位

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = getattr(self.request, 'user', None)
        if user and user.is_authenticated and user.role == UserRole.ADMIN:
            self.filters['user_id'] = filters.ModelChoiceFilter(queryset=User.objects.all())
# ------------------------filter-end------------------------------


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