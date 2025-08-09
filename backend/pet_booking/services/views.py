from rest_framework import viewsets
from .models import BoardingService, GroomingService, BoardingServicePricing, GroomingServicePricing
from .serializers import BoardingServiceSerializer, GroomingServiceSerializer, BoardingServicePricingSerializer, GroomingServicePricingSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class BoardingServiceViewSet(viewsets.ModelViewSet):
    queryset = BoardingService.objects.all()
    serializer_class = BoardingServiceSerializer
    # permission_classes = [IsAuthenticated]

class BoardingServicePricingViewset(viewsets.ModelViewSet):
    queryset = BoardingServicePricing.objects.all()
    serializer_class = BoardingServicePricingSerializer
    # permission_classes = [IsAuthenticated]

class GroomingServiceViewSet(viewsets.ModelViewSet):
    queryset = GroomingService.objects.all()
    serializer_class = GroomingServiceSerializer
    # permission_classes = [IsAuthenticated]

class GroomingServicePricingViewset(viewsets.ModelViewSet):
    queryset = GroomingServicePricing.objects.all()
    serializer_class = GroomingServicePricingSerializer
    # permission_classes = [IsAuthenticated]