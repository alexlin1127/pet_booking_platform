# third-party
from rest_framework import serializers

# app
from .models import ReservationBoarding, ReservationGrooming, Orders, GroomingSchedules, BoardingSchedules

class ReservationGroomingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationGrooming
        fields = '__all__'

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
    reservation_grooming_detail = ReservationGroomingSerializer(
        source='reservation_grooming',
        read_only=True
    )

    reservation_boarding_detail = ReservationBoardingSerializer(
        source='reservation_boarding',
        read_only=True
    )

    class Meta:
        model = Orders
        fields = '__all__'
