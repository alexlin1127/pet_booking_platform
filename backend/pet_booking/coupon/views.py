from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from .models import Coupon

# Create your views here.

class CouponViewSet(ViewSet):
    def get_remaining_coupons(self, request):
        used_coupons_count = Coupon.objects.filter(status='used').count()
        remaining_coupons = 84 - used_coupons_count
        return Response({"remaining_coupons": remaining_coupons})
