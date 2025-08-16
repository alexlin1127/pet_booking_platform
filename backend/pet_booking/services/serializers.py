from rest_framework import serializers
from .models import BoardingService, BoardingServicePricing, GroomingService, GroomingServicePricing

# 住宿
class BoardingServicePricingSerializer(serializers.ModelSerializer):
    boarding_service = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = BoardingServicePricing
        fields = '__all__'

class BoardingServiceSerializer(serializers.ModelSerializer):
    store_id = serializers.PrimaryKeyRelatedField(read_only=True)
    pricings = BoardingServicePricingSerializer(source='boardingservicepricing_set', many=True)

    class Meta:
        model = BoardingService
        fields = ['id', 'store_id', 'species', 'cleaning_frequency', 'room_type', 'room_count', 'pet_available_amount', 'introduction', 'created_at', 'updated_at', 'pricings', 'notice']

    def create(self, validated_data):
        pricings_data = validated_data.pop('boardingservicepricing_set', [])
        service = BoardingService.objects.create(**validated_data)
        for pricing_data in pricings_data:
            BoardingServicePricing.objects.create(boarding_service=service, **pricing_data)
        return service

    def update(self, instance, validated_data):
        pricings_data = validated_data.pop('boardingservicepricing_set', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        instance.boardingservicepricing_set.all().delete()
        for pricing_data in pricings_data:
            BoardingServicePricing.objects.create(boarding_service=instance, **pricing_data)
        return instance




# 美容
class GroomingServicePricingSerializer(serializers.ModelSerializer):
    grooming_service_id = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = GroomingServicePricing
        fields = '__all__'

class GroomingServiceSerializer(serializers.ModelSerializer):
    store_id = serializers.PrimaryKeyRelatedField(read_only=True)
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
        fields = ['id', 'store_id','species', 'service_title', 'introduction', 'notice', 'duration_min', 'duration_max', 'created_at', 'updated_at', 'pricings']

    def create(self, validated_data):
        pricings_data = validated_data.pop('groomingservicepricing_set', [])
        service = GroomingService.objects.create(**validated_data)
        for pricing_data in pricings_data:
            GroomingServicePricing.objects.create(grooming_service_id=service, **pricing_data)
        return service
    
    def update(self, instance, validated_data):
        pricings_data = validated_data.pop('groomingservicepricing_set', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        instance.groomingservicepricing_set.all().delete()
        for pricing_data in pricings_data:
            GroomingServicePricing.objects.create(grooming_service_id=instance, **pricing_data)
        return instance
