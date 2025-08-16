from django.db import models
from pet_booking.users.models import User
import uuid


class CouponStatus(models.TextChoices):
    USED = 'used', '已使用'
    NOT_USED = 'not_used', '未使用'


class Coupon(models.Model):
    user_id = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        to_field='user_id',
        db_column='user_id',
        verbose_name="用戶ID"
    )
    store_id = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="店家ID"
    )
    coupon_number = models.CharField(
        max_length=100, 
        unique=True, 
        verbose_name="優惠券號碼"
    )
    reservation_id = models.CharField(
        max_length=100, 
        null=True, 
        blank=True, 
        verbose_name="預約ID"
    )
    order_id = models.CharField(
        max_length=100, 
        null=True, 
        blank=True, 
        verbose_name="訂單ID"
    )
    status = models.CharField(
        max_length=20,
        choices=CouponStatus.choices,
        default=CouponStatus.NOT_USED,
        verbose_name="使用狀態"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新時間")

    class Meta:
        verbose_name = "優惠券"
        verbose_name_plural = "優惠券"
        db_table = 'coupons'

    def __str__(self):
        return f"{self.coupon_number} - {self.user_id.username} ({self.get_status_display()})"
