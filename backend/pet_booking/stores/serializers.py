from rest_framework import serializers
from .models import Store, StoreImage, Post
from users.models import User

class StoreSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user_id.username', read_only=True)

    class Meta:
        model = Store
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class StoreImageSerializer(serializers.ModelSerializer):
    store_name = serializers.CharField(source='store_id.store_name', read_only=True)

    class Meta:
        model = StoreImage
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    store_name = serializers.CharField(source='store_id.store_name', read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


