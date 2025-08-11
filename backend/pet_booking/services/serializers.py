from rest_framework import serializers
from .models import BoardingService,BoardingRoomPricing, BoardingRoomType, GroomingService, GroomingServicePricing   


# 住宿
class BoardingRoomPricingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardingRoomPricing
        fields = '__all__'

class BoardingRoomTypeSerializer(serializers.ModelSerializer):
    pricings = BoardingRoomPricingSerializer(source='boardingroompricing_set', many=True)

    class Meta:
        model = BoardingRoomType
        fields = ['id', 'boarding_service', 'species', 'room_type', 'room_count', 'pet_available_amount', 'pricings']

class BoardingServiceSerializer(serializers.ModelSerializer):
    rooms = BoardingRoomTypeSerializer(source='boardingroomtype_set', many=True)

    class Meta:
        model = BoardingService
        fields = ['id', 'store_id', 'cleaning_frequency', 'introduction', 'created_at', 'updated_at', 'rooms']

    def create(self, validated_data):
        rooms_data = validated_data.pop('rooms', [])
        service = BoardingService.objects.create(**validated_data)
        for room_data in rooms_data:
            pricings_data = room_data.pop('pricings', [])
            room = BoardingRoomType.objects.create(boarding_service=service, **room_data)
            for pricing_data in pricings_data:
                BoardingRoomPricing.objects.create(room_type=room, **pricing_data)
        return service

    def update(self, instance, validated_data):
        rooms_data = validated_data.pop('rooms', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        instance.boardingroomtype_set.all().delete()
        for room_data in rooms_data:
            pricings_data = room_data.pop('pricings', [])
            room = BoardingRoomType.objects.create(boarding_service=instance, **room_data)
            for pricing_data in pricings_data:
                BoardingRoomPricing.objects.create(room_type=room, **pricing_data)
        return instance
  


# 美容
class GroomingServicePricingSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroomingServicePricing
        fields = '__all__'

class GroomingServiceSerializer(serializers.ModelSerializer):
    pricings = GroomingServicePricingSerializer(source='groomingservicepricing_set', many=True)
    duration_min = serializers.SerializerMethodField()
    duration_max = serializers.SerializerMethodField()

    def get_duration_min(self, obj):
        durations = obj.groomingservicepricing_set.values_list('grooming_duration', flat=True)
        return min(durations) if durations else None

    def get_duration_max(self, obj):
        durations = obj.groomingservicepricing_set.values_list('grooming_duration', flat=True)
        return max(durations) if durations else None

    class Meta:
        model = GroomingService
        fields = ['id', 'store_id', 'service_title', 'introduction', 'notice', 'duration_min', 'duration_max', 'created_at', 'updated_at', 'pricings']

    def create(self, validated_data):
        pricings_data = validated_data.pop('pricings', [])
        service = GroomingService.objects.create(**validated_data)
        for pricing_data in pricings_data:
            GroomingServicePricing.objects.create(grooming_service_id=service, **pricing_data)
        return service
    
    def update(self, instance, validated_data):
        pricings_data = validated_data.pop('pricings', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        instance.groomingservicepricing_set.all().delete()
        for pricing_data in pricings_data:
            GroomingServicePricing.objects.create(grooming_service_id=instance, **pricing_data)
        return instance
