# users/views.py
from django.utils.timezone import now
from django.db.models.functions import TruncDate
from django.db.models import Count
from rest_framework import viewsets, status
from rest_framework.permissions import BasePermission, AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import PageNumberPagination
# from django_filters import rest_framework as filter
from django_filters.rest_framework import DjangoFilterBackend
from datetime import timedelta
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


    @action(detail=False, methods=['get'], url_path='registered_all')
    def registered_all(self, request):
        """
        一個 API 回傳全部：
        - 總數（所有 / 近7天 / 近30天）
        - 會員 & 店家近7日每日註冊數
        - 會員 & 店家近30日每日註冊數
        只有 Admin 可用
        """
        if not (request.user.is_authenticated and request.user.role == UserRole.ADMIN):
            return Response({'detail': '沒有權限'}, status=status.HTTP_403_FORBIDDEN)

        today = now().date()
        qs = User.objects.all()

        # 共用每日計數方法
        def get_daily_counts(role, days):
            start_date = today - timedelta(days=days)
            daily_qs = qs.filter(role=role, created_at__date__gte=start_date)
            daily_counts = daily_qs.annotate(date=TruncDate('created_at')) \
                                   .values('date') \
                                   .annotate(count=Count('id')) \
                                   .order_by('date')
            date_to_count = {item['date']: item['count'] for item in daily_counts}
            all_days = [today - timedelta(days=i) for i in reversed(range(days))]
            return [
                {'date': d.isoformat(), 'count': date_to_count.get(d, 0)} for d in all_days
            ]

        # 總數計算
        all_member = qs.filter(role=UserRole.MEMBER).count()
        all_store = qs.filter(role=UserRole.STORE).count()

        # 近7天總數
        start_7 = today - timedelta(days=7)
        last7_member = qs.filter(role=UserRole.MEMBER, created_at__date__gte=start_7).count()
        last7_store = qs.filter(role=UserRole.STORE, created_at__date__gte=start_7).count()

        # 近30天總數
        start_30 = today - timedelta(days=30)
        last30_member = qs.filter(role=UserRole.MEMBER, created_at__date__gte=start_30).count()
        last30_store = qs.filter(role=UserRole.STORE, created_at__date__gte=start_30).count()

        # 每日統計
        member_daily_7 = get_daily_counts(UserRole.MEMBER, 7)
        store_daily_7 = get_daily_counts(UserRole.STORE, 7)
        member_daily_30 = get_daily_counts(UserRole.MEMBER, 30)
        store_daily_30 = get_daily_counts(UserRole.STORE, 30)

        return Response({
            'summary': {
                'all': {
                    'member_count': all_member,
                    'store_count': all_store
                },
                'last_7_days': {
                    'member_count': last7_member,
                    'store_count': last7_store
                },
                'last_30_days': {
                    'member_count': last30_member,
                    'store_count': last30_store
                }
            },
            'daily_registration_last_7_days': {
                'member': member_daily_7,
                'store': store_daily_7
            },
            'daily_registration_last_30_days': {
                'member': member_daily_30,
                'store': store_daily_30
            }
        })
