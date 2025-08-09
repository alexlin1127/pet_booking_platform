from rest_framework import serializers
from .models import Store, StoreImage, Post
from users.models import User

# 店家資訊圖片集
class StoreImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreImage
        fields = '__all__'

# 店家詳細頁
class StoreSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user_id.username', read_only=True)
    images = StoreImageSerializer(source='images', many=True, read_only=True)

    class Meta:
        model = Store
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


# 管理者-店家清單
class StoreListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user_id.username', read_only=True)
    
    class Meta:
        model = Store
        fields = ['user_id', 'store_name', 'owner_name', 'address', 'phone', 'created_at', 'status', 'grooming_service', 'boarding_service']
        

# 管理者-店家詳細
class StoreDetailSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user_id.username', read_only=True)

    class Meta:
        model = Store
        fields = ['user_id', 'store_name', 'owner_name', 'address', 'phone', 'email','pick_up_service', 'created_at', 'status', 'grooming_service', 'boarding_service', 'staff_number', 'business_licences_url', 'boarding_license_dog_url', 'boarding_license_cat_url', 'grooming_single_appointment', 'reject_content']



# 店家貼文頁
class PostSerializer(serializers.ModelSerializer):
    store_name = serializers.CharField(source='store.store_name', read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


