# users/models.py
import time
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class UserRole(models.TextChoices):
    MEMBER = 'member', '一般會員'   
    STORE = 'store', '寵物業者'
    ADMIN = 'admin', '系統管理者'

class User(AbstractUser):
    user_id = models.CharField(max_length=64, blank=True, null=True, unique=True)
    role = models.CharField(max_length=64, choices=UserRole.choices, default=UserRole.MEMBER, blank=False, verbose_name="用戶角色")
    is_store_owner = models.BooleanField(default=False, blank=False, null=False, verbose_name="是否為寵物業者")
    is_admin = models.BooleanField(default=False, blank=False, null=False, verbose_name="是否為系統管理者")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新時間")

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    ROLE_PREFIX = {
        'member': 'M',
        'store': 'S',
        'admin': 'A',
    }

    def save(self, *args, **kwargs):
        if not self.user_id and self.role:
            prefix = self.ROLE_PREFIX.get(self.role, 'X')  # 如果沒找到對應角色，給預設字母 X
            now_timestamp = int(time.time())
            self.user_id = f"{prefix}{now_timestamp}"
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "用戶"
        verbose_name_plural = "用戶"
        db_table = 'users'

    def __str__(self):
        return f"{self.username}-{self.role}"