# apps/users/views.py
from rest_framework import viewsets, status
from rest_framework.permissions import BasePermission, AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import PageNumberPagination
# from django_filters import rest_framework as filter
from django_filters.rest_framework import DjangoFilterBackend
from .models import User, UserRole
from .serializers import UserSerializer
# Create your views here.

class IsAdminOrSelf(BasePermission):
    """
    只允許 admin 查看/修改/刪除任何人，其他角色只能操作自己。
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and request.user.role == UserRole.ADMIN:
            return True
        return obj == request.user
    
class IsAdminForList(BasePermission):
    """
    限制只有 admin 才能使用 list API（GET /users/）
    """
    def has_permission(self, request, view):
        if view.action == 'list':
            if not request.user.is_authenticated or request.user.role != UserRole.ADMIN:
                # 這裡直接丟出自訂 403 訊息
                raise PermissionDenied(detail="只有系統管理者能查看所有使用者資料")
        return True

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10              # 每頁顯示 10 筆
    page_size_query_param = 'page_size'  # 可用 URL ?page_size=20 動態調整
    max_page_size = 50         # 最大每頁顯示數

class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    # queryset =User.objects.all().order_by('-user_id')
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['role']  # 可根據需求增加欄位
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.role == UserRole.ADMIN:
            # Admin 看全部
            return User.objects.all().order_by('-user_id')
        # 其他角色只能查自己
        return User.objects.filter(pk=user.pk)
    
    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = [AllowAny]
        elif self.action in ['list']:
            permission_classes = [IsAuthenticated, IsAdminForList]
        elif self.action in ['me']:  # /users/me/ 只要登入即可
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsAdminOrSelf]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get', 'patch', 'delete'], url_path='me')
    def me(self, request):
        """
        GET    /users/me/    取得自己資料
        PATCH  /users/me/    部分更新自己資料（包含密碼）
        DELETE /users/me/    刪除自己帳號
        """
        if request.method.lower() == 'get':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)

        elif request.method.lower() == 'patch':
            serializer = self.get_serializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()  # 會自動呼叫 serializer 的 update，包含密碼加密
            return Response(serializer.data)

        elif request.method.lower() == 'delete':
            request.user.delete()
            return Response(
                {"detail": "帳號已刪除"},
                status=status.HTTP_204_NO_CONTENT
            )
        
    def create(self, request, *args, **kwargs):
        print(request.data)
        request_data = request.data
        serializer = self.get_serializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()