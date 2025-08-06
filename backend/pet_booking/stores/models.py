from django.db import models
from users.models import User
from reservations.models import Order

# Create your models here.
class Store(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    store_name = models.CharField(max_length=100)
    owner_name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    email = models.EmailField()
    description = models.TextField()
    phone = models.CharField(max_length=20)
    staff_number = models.IntegerField(null=True, blank=True)
    pick_up_service = models.BooleanField(default=False)
    grooming_service = models.BooleanField(default=False)
    boarding_service = models.BooleanField(default=False)
    business_licences_url = models.ImageField(upload_to='stores/', blank=True, null=True)
    boarding_license_dog_url = models.ImageField(upload_to='stores/', blank=True, null=True)
    boarding_license_cat_url = models.ImageField(upload_to='stores/', blank=True, null=True)
    groomimg_single_appointment = models.BooleanField(default=False)
    working_day = models.JSONField(null=True, blank=True)
    daily_opening_time = models.TimeField()
    daily_closing_hours = models.TimeField()
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('confirmed', 'Confirmed')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.store_name


class StoreImage(models.Model):
    store_id = models.ForeignKey(Store, on_delete=models.CASCADE)
    image_url = models.ImageField(upload_to='stores/', blank=True, null=True)

    def __str__(self):
        return f"Image for {self.store_id.store_name}"

class Post(models.Model):
    store_id = models.ForeignKey(Store, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    image_url = models.ImageField(upload_to='posts/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('confirmed', 'Confirmed')])
    tags = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.store_id.store_name} - {self.title}"

class CustomerNote(models.Model):
    store_id = models.ForeignKey(Store, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.ForeignKey('Order', on_delete=models.SET_NULL, null=True)
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Note for {self.user_id.username} by {self.store_id.store_name}"