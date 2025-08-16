# third-party
from rest_framework import serializers

# app
from .models import ReservationBoarding, ReservationGrooming, Orders, GroomingSchedules, BoardingSchedules
from pet_booking.users.models import User

class ReservationGroomingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationGrooming
        fields = '__all__'

class StoreNoteUpdateSerializer(serializers.Serializer):
    reservation_id = serializers.CharField(max_length=20, required=True)
    store_note = serializers.CharField(max_length=1000, required=True, allow_blank=True)
    def validate_reservation_id(self, value):
        """驗證 reservation_id 是否存在"""
        try:
            ReservationGrooming.objects.get(reservation_id=value)
        except ReservationGrooming.DoesNotExist:
            raise serializers.ValidationError("Reservation not found")
        return value

class BoardingStoreNoteUpdateSerializer(serializers.Serializer):
    reservation_id = serializers.CharField(max_length=20, required=True)
    store_note = serializers.CharField(max_length=1000, required=True, allow_blank=True)

    def validate_reservation_id(self, value):
        """驗證 reservation_id 是否存在"""
        try:
            ReservationBoarding.objects.get(reservation_id=value)
        except ReservationBoarding.DoesNotExist:
            raise serializers.ValidationError("Reservation not found")
        return value
    
class ReservationBoardingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationBoarding
        fields = '__all__'

class GroomingSchedulesSerializer(serializers.ModelSerializer):
    reservation_grooming_detail = ReservationGroomingSerializer(
        source='reservation_grooming_id',
        read_only=True
    )

    class Meta:
        model = GroomingSchedules
        fields = '__all__'

class BoardingSchedulesSerializer(serializers.ModelSerializer):
    reservation_boarding_detail = ReservationBoardingSerializer(
        source='reservation_boarding_id',
        read_only=True
    )

    class Meta:
        model = BoardingSchedules
        fields = '__all__'

class OrdersSerializer(serializers.ModelSerializer):
    reservation_grooming_id = serializers.CharField(
        max_length=50,
        required=False,
        allow_blank=True
    )
    reservation_boarding_id = serializers.CharField(
        max_length=50,
        required=False,
        allow_blank=True
    )
    blacklist = serializers.BooleanField(
        required=True
    )

    class Meta:
        model = Orders
        fields = ['reservation_grooming_id', 'reservation_boarding_id', 'user_id', 'total_price', 'status', 'blacklist']

    def validate(self, data):
        if data.get('reservation_grooming_id') and data.get('reservation_boarding_id'):
            raise serializers.ValidationError("Only one of reservation_grooming_id or reservation_boarding_id can be set.")
        
        if not isinstance(data.get('blacklist'), bool):
            raise serializers.ValidationError("Blacklist must be a boolean value.")
        
        return data