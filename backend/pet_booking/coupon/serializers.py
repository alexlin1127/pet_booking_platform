from rest_framework import serializers
from .models import Coupon
from pet_booking.users.models import User


class CouponSerializer(serializers.ModelSerializer):
    """優惠券序列化器"""
    
    class Meta:
        model = Coupon
        fields = [
            'id',
            'user_id',
            'coupon_number',
            'status'
        ]
        read_only_fields = ['id', 'coupon_number']

class CouponClaimSerializer(serializers.Serializer):
    """領取優惠券的序列化器"""
    user_id = serializers.CharField(max_length=64)

    def validate_user_id(self, value):
        """驗證用戶是否存在且未領取過優惠券"""
        try:
            user = User.objects.get(user_id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("用戶不存在")
        
        # 檢查用戶是否已經有優惠券
        if Coupon.objects.filter(user_id=user).exists():
            raise serializers.ValidationError("用戶已經領取過優惠券")
        
        return value


class CouponReservationSerializer(serializers.Serializer):
    """預約完成時更新優惠券的序列化器"""
    user_id = serializers.CharField(max_length=64)
    reservation_id = serializers.CharField(max_length=100)

    def validate_user_id(self, value):
        """驗證用戶是否存在"""
        try:
            User.objects.get(user_id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("用戶不存在")
        return value

    def validate(self, data):
        """驗證用戶是否有未使用的優惠券"""
        user_id = data.get('user_id')
        try:
            user = User.objects.get(user_id=user_id)
            coupon = Coupon.objects.get(user_id=user, status='not_used')
        except Coupon.DoesNotExist:
            raise serializers.ValidationError("用戶沒有可用的優惠券")
        
        return data


class CouponCompleteOrderSerializer(serializers.Serializer):
    """完成訂單時使用優惠券的序列化器"""
    reservation_id = serializers.CharField(max_length=100)
    order_id = serializers.CharField(max_length=100)

    def validate_reservation_id(self, value):
        """驗證預約ID對應的優惠券是否存在"""
        try:
            coupon = Coupon.objects.get(reservation_id=value, status='not_used')
        except Coupon.DoesNotExist:
            raise serializers.ValidationError("找不到對應的可用優惠券")
        return value


class CouponStatsSerializer(serializers.Serializer):
    """優惠券統計序列化器"""
    total_limit = serializers.IntegerField(default=84, read_only=True)
    used_count = serializers.IntegerField(read_only=True)
    remaining_count = serializers.IntegerField(read_only=True)


class CouponListSerializer(serializers.ModelSerializer):
    """優惠券列表序列化器"""
    user_username = serializers.CharField(source='user_id.username', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Coupon
        fields = [
            'id',
            'user_username',
            'coupon_number',
            'status',
            'created_at'
        ]
