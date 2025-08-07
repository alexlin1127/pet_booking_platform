from django.db import models


# Create your models here.
class Store(models.Model):
    user_id = models.ForeignKey('users.User',to_field='user_id', on_delete=models.CASCADE)
    store_name = models.CharField(max_length=100)
    owner_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=20)
    staff_number = models.IntegerField(null=True, blank=True)
    pick_up_service = models.BooleanField(default=False)
    grooming_service = models.BooleanField(default=False)
    boarding_service = models.BooleanField(default=False)
    business_licences_url = models.ImageField(upload_to='stores/', blank=True, null=True)
    boarding_license_dog_url = models.ImageField(upload_to='stores/', blank=True, null=True)
    boarding_license_cat_url = models.ImageField(upload_to='stores/', blank=True, null=True)
    grooming_single_appointment = models.BooleanField(default=False)
    daily_opening_time = models.TimeField(blank=True, null=True)
    daily_closing_hours = models.TimeField(blank=True, null=True)
    close_day = models.JSONField(null=True, blank=True)
    service_item = models.JSONField(null=True, blank=True)
    traffic_info = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('repending', 'Repending'), ('rechecked', 'Rechecked'), ('confirmed', 'Confirmed')])
    reject_content = models.CharField(max_length=1024, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    line_link = models.URLField(blank=True, null=True, max_length=200)
    facebook_link = models.URLField(blank=True, null=True, max_length=200)
    google_map_link = models.URLField(blank=True, null=True, max_length=200)


    def __str__(self):
        return self.store_name


class StoreImage(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE , related_name='images')
    image_url = models.ImageField(upload_to='stores/', blank=True, null=True)

    def __str__(self):
        return f"Image for {self.store_id.store_name}"

class Post(models.Model):
    store_id = models.ForeignKey(Store, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=500)
    image_url = models.ImageField(upload_to='posts/', blank=True, null=True, max_length=200)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('repending', 'Repending'), ('rechecked', 'Rechecked'), ('confirmed', 'Confirmed')])
    tags = models.JSONField(null=True, blank=True)
    reject_content = models.CharField(max_length=1024, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.store_id.store_name} - {self.title}"

