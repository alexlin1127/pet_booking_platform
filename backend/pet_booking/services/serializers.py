from rest_framework import serializers
from .models import BoardingService, BoardingServicePricing, GroomingService, GroomingServicePricing   

class BoardingServicePricingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardingServicePricing
        fields = '__all__'

class BoardingServiceSerializer(serializers.ModelSerializer):
    pricings = BoardingServicePricingSerializer(source='boardingservicepricing_set', many=True)
    duration_min = serializers.SerializerMethodField()
    duration_max = serializers.SerializerMethodField()

    class Meta:
        model = BoardingService
        fields = ['id', 'store_id', 'cleaning_frequency', 'introduction', 'created_at', 'updated_at', 'pricings', 'duration_min', 'duration_max']
    
    def get_duration_min(self, obj):
        durations = obj.boardingservicepricing_set.values_list('duration', flat=True)
        return min(durations) if durations else None

    def get_duration_max(self, obj):
        durations = obj.boardingservicepricing_set.values_list('duration', flat=True)
        return max(durations) if durations else None
    
    def create(self, validated_data):
        pricings_data = validated_data.pop('pricings')
        service = BoardingService.objects.create(**validated_data)
        for pricing_data in pricings_data:
            BoardingServicePricing.objects.create(boarding_service_id=service, **pricing_data)
        return service

    def update(self, instance, validated_data):
        pricings_data = validated_data.pop('pricings')
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        instance.boardingservicepricing_set.all().delete()
        for pricing_data in pricings_data:
            BoardingServicePricing.objects.create(boarding_service_id=instance, **pricing_data)
        return instance
  
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
        fields = ['id', 'store_id', 'service_title', 'introduction', 'notice', 'duration_minutes_min', 'duration_minutes_max', 'created_at', 'updated_at', 'pricings']

    def create(self, validated_data):
        pricings_data = validated_data.pop('pricings')
        service = GroomingService.objects.create(**validated_data)
        for pricing_data in pricings_data:
            GroomingServicePricing.objects.create(grooming_service_id=service, **pricing_data)
        return service
    
    def update(self, instance, validated_data):
        pricings_data = validated_data.pop('pricings')
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        instance.groomingservicepricing_set.all().delete()
        for pricing_data in pricings_data:
            GroomingServicePricing.objects.create(grooming_service_id=instance, **pricing_data)
        return instance
