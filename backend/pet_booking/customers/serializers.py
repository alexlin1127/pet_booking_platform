from rest_framework import serializers
from users.models import User
from stores.models import Store
from .models import CustomersProfile, LikeStore, Pet
from stores.serializers import StoreSerializer

class CustomersProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.SlugRelatedField(
        slug_field='user_id',
        queryset=User.objects.all()
    )

    class Meta:
        model = CustomersProfile
        fields = (
            'id',
            'user_id',
            'full_name',
            'gender',
            'phone',
            'email',
            'address',
        )

class LikeStoreSerializer(serializers.ModelSerializer):
    user_id = serializers.SlugRelatedField(
        slug_field='user_id',
        queryset=User.objects.all()
    )
    
    store_id = serializers.SlugRelatedField(
        slug_field='store_name',
        queryset=Store.objects.all(),
        write_only=True
    )
    
    store = StoreSerializer(read_only=True, source='store_id')
    
    class Meta:
        model = LikeStore
        fields = ('id', 'user_id', 'store', 'store_id')

class PetSerializer(serializers.ModelSerializer):
    user_id = serializers.SlugRelatedField(
        slug_field='user_id',
        queryset=User.objects.all()
    )
    
    class Meta:
        model = Pet
        fields = (
            'id',
            'user_id',
            'species',
            'name',
            'gender',
            'breed',
            'age',
            'weight',
            'spayed_or_neutered',
            'microchip',
            'last_deworming_date',
            'last_vaccine_date',
            'notes',
            'image_url',
            'created_at',
        )
        read_only_fields = ('created_at',)
