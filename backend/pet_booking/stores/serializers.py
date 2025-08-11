from rest_framework import serializers
from .models import Store, StoreImage, Post
from pet_booking.users.models import User

# 店家資訊圖片集
class StoreImageSerializer(serializers.ModelSerializer):
    store = serializers.PrimaryKeyRelatedField(read_only=True)
    image_url = serializers.ImageField()
    class Meta:
        model = StoreImage
        fields = '__all__'

    def validate(self, attrs):
        store = attrs.get('store')
        if store and store.images.count() >= 8:
            raise serializers.ValidationError("最多只能上傳8張圖片")
        return attrs

# 店家詳細頁
class StoreSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.CharField(source='user_id.username', read_only=True)
    images = StoreImageSerializer(many=True, required=False)

    class Meta:
        model = Store
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        store = Store.objects.create(**validated_data)
        for image_data in images_data:
            StoreImage.objects.create(store=store, **image_data)
        return store

    def update(self, instance, validated_data):
        # 更新其他欄位
        images_data = validated_data.pop('images', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        
        # 刪除舊圖片
        instance.images.all().delete()

        # 從 request.FILES 取得圖片檔案
        files = self.context['request'].FILES.getlist('images')
        for image_file in files:
            StoreImage.objects.create(store=instance, image_url=image_file)

        return instance


# 管理者-店家清單
class StoreListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user_id.username', read_only=True)
    
    class Meta:
        model = Store
        fields = ['user_id','username', 'store_name', 'owner_name', 'address', 'phone', 'created_at', 'status', 'grooming_service', 'boarding_service', 'service_item', 'hero_image']
        

# 管理者-店家詳細
class StoreDetailSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user_id.username', read_only=True)

    class Meta:
        model = Store
        fields = ['user_id','username', 'store_name', 'owner_name', 'address', 'phone', 'email','pick_up_service', 'created_at', 'status', 'grooming_service', 'boarding_service', 'staff_number', 'business_licences_url', 'boarding_license_dog_url', 'boarding_license_cat_url', 'grooming_single_appointment', 'reject_content']



# 店家貼文頁
class PostSerializer(serializers.ModelSerializer):
    store = serializers.PrimaryKeyRelatedField(read_only=True)
    store_name = serializers.CharField(source='store.store_name', read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


