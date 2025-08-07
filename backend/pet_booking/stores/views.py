from rest_framework import viewsets
from .models import Store, Post
from .serializers import StoreSerializer, PostSerializer
from django_filters import rest_framework as filter
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class StautusFilter(filter.FilterSet):
    class Meta:
        model = Store
        fields = ['status']


# 店家
class StoreProfileViewSet(viewsets.ModelViewSet):
    serializer_class = StoreSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Store.objects.filter(user_id=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user_id=self.request.user)
    
# 店家文章
class StorePostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(store_id__user_id=self.request.user)

    def perform_create(self, serializer):
        store = Store.objects.get(user_id=self.request.user)
        serializer.save(store_id=store)

    def perform_update(self, serializer):
        store = Store.objects.get(user_id=self.request.user)
        serializer.save(store_id=store)


# 管理者
class StoreAdminViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    filterset_class= StautusFilter
    permission_classes = [IsAuthenticated]


# 管理者文章
class AdminPostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filterset_fields = ['status']
    permission_classes = [IsAuthenticated]

