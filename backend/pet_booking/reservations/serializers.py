# third-party
from rest_framework import serializers

# app
from .models import Reservation_boarding, Reservation_grooming, Orders, Grooming_schedules, Boarding_schedules

class Reservation_grooming_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation_grooming
        fields = '__all__'

class Reservation_boarding_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation_boarding
        fields = '__all__'

class Grooming_schedules_Serializer(serializers.ModelSerializer):
    Reservation_grooming_detail = Reservation_grooming_Serializer(
        source = 'reservation_grooming',
        read_only = True
    )

    class Meta:
        model = Grooming_schedules
        fields = '__all__'

class Boarding_schedules_Serializer(serializers.ModelSerializer):
    reservation_boarding_detail = Reservation_boarding_Serializer(
        source = 'reservation_boarding',
        read_only = True
    )

    class Meta:
        model = Boarding_schedules
        fields = '__all__'

class Orders_Serializer(serializers.ModelSerializer):
    reservation_grooming_detail = Reservation_grooming_Serializer(
        source = 'reservation_grooming_id',
        read_only = True
    )

    reservation_boarding_detail = Reservation_boarding_Serializer(
        source = 'reservation_boarding_id',
        read_only = True
    )
    
    class Meta:
        model = Orders
        fields = '__all__'
