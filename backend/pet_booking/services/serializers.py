from rest_framework import serializers
from .models import BoardingService, BoardingServicePricing, GroomingService, GroomingServicePricing   

class BoardingServicePricingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardingServicePricing
        fields = '__all__'

class BoardingServiceSerializer(serializers.ModelSerializer):
    pricings = BoardingServicePricingSerializer(source='boardingservicepricing_set', many=True)

    class Meta:
        model = BoardingService
        fields = ['id', 'store_id', 'cleaning_frequency', 'introduction', 'created_at', 'updated_at', 'pricings']

    def create(self, validated_data):
        pricings_data = validated_data.pop('pricings')
        service = BoardingService.objects.create(**validated_data)
        for pricing_data in pricings_data:
            BoardingServicePricing.objects.create(boarding_service_id=service, **pricing_data)
        return service

  
class GroomingServicePricingSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroomingServicePricing
        fields = '__all__'

class GroomingServiceSerializer(serializers.ModelSerializer):
    pricings = GroomingServicePricingSerializer(source='groomingservicepricing_set', many=True)

    class Meta:
        model = GroomingService
        fields = ['id', 'store_id', 'service_title', 'introduction', 'notice', 'duration_minutes_min', 'duration_minutes_max', 'created_at', 'updated_at', 'pricings']

    def create(self, validated_data):
        pricings_data = validated_data.pop('pricings')
        service = GroomingService.objects.create(**validated_data)
        for pricing_data in pricings_data:
            GroomingServicePricing.objects.create(grooming_service_id=service, **pricing_data)
        return service
    
