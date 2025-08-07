from rest_framework import serializers
from .models import BoardingService, BoardingServicePricing, GroomingService, GroomingServicePricing   

class BoardingServicePricingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardingServicePricing
        fields = '__all__'

class BoardingServiceSerializer(serializers.ModelSerializer):
    pricings = BoardingServicePricingSerializer(source='boardingservicepricing_set',many=True, read_only=True)

    class Meta:
        model = BoardingService
        fields = ['id', 'store_id', 'cleaning_frequency', 'introduction', 'created_at', 'updated_at', 'pricings']


class GroomingServicePricingSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroomingServicePricing
        fields = '__all__'

class GroomingServiceSerializer(serializers.ModelSerializer):
    pricings = GroomingServicePricingSerializer(source='groomingservicepricing_set', many=True, read_only=True)

    class Meta:
        model = GroomingService
        fields = ['id', 'store_id', 'service_title', 'introduction', 'notice', 'duration_minutes_min', 'duration_minutes_max', 'created_at', 'updated_at', 'pricings']
