from rest_framework import serializers
from .models import Store, StoreImage, Post
from users.models import User


class StoreImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreImage
        fields = '__all__'


class StoreSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user_id.username', read_only=True)
    images = StoreImageSerializer(many=True, read_only=True)

    class Meta:
        model = Store
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class PostSerializer(serializers.ModelSerializer):
    store_name = serializers.CharField(source='store_id.store_name', read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


