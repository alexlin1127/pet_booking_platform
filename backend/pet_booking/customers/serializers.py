# customers/serializers.py
from rest_framework import serializers
# from pet_booking.users.models import User
from pet_booking.stores.models import Store
from .models import CustomersProfile, LikeStore, Pet
from pet_booking.stores.serializers import StoreSerializer

class RegisterSendCodeSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.CharField()

class RegisterConfirmCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()

# -------------------------------------------------------------

class CustomersProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.SlugRelatedField(
        slug_field='user_id',
        # queryset=User.objects.all(),
        read_only=True
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
        # queryset=User.objects.all(),
        read_only=True
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
        # queryset=User.objects.all(),
        read_only=True
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
            'size',
            'fur_amount',
            'spayed_or_neutered',
            'microchip',
            'last_deworming_date',
            'last_vaccine_date',
            'notes',
            'image_url',
            'created_at',
        )
        read_only_fields = ('created_at',)
