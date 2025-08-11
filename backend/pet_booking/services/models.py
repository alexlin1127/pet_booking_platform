from django.db import models


# Create your models here.
# 住宿
class BoardingService(models.Model):
    store_id = models.ForeignKey('stores.Store', on_delete=models.CASCADE)
    cleaning_frequency = models.CharField(max_length=32)
    introduction = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Boarding Service at {self.store_id.store_name}"


class BoardingRoomType(models.Model):
    boarding_service = models.ForeignKey(BoardingService, on_delete=models.CASCADE)
    species = models.CharField(max_length=10, choices=[('cat', 'Cat'), ('dog', 'Dog')])
    room_type = models.CharField(max_length=100)
    room_count = models.IntegerField()
    pet_available_amount = models.IntegerField()


class BoardingRoomPricing(models.Model):
    room_type = models.ForeignKey(BoardingRoomType, on_delete=models.CASCADE)
    duration = models.IntegerField()
    duration_unit = models.CharField(max_length=10, choices=[('day', 'Day'), ('month', 'Month')])
    pricing = models.IntegerField()
    overtime_rate = models.IntegerField()
    overtime_charging = models.BooleanField(default=False)

# 美容
class GroomingService(models.Model):
    store_id = models.ForeignKey('stores.Store', on_delete=models.CASCADE)
    species = models.CharField(max_length=10, choices=[('cat', 'Cat'), ('dog', 'Dog')])
    service_title = models.CharField(max_length=64)
    introduction = models.TextField(max_length=500)
    notice = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Grooming Service: {self.service_title} at {self.store_id.store_name}"

class GroomingServicePricing(models.Model):
    grooming_service_id = models.ForeignKey(GroomingService, on_delete=models.CASCADE)
    pet_size = models.CharField(max_length=10, choices=[('small', 'Small'), ('medium', 'Medium'), ('large', 'Large'), ('other', 'Other')])
    fur_amount = models.CharField(max_length=16, choices = [('none', '無毛'),('short', '短毛'),('medium', '中毛'),('long', '長毛'),('other', '其他'),])
    pricing = models.IntegerField()
    grooming_duration = models.IntegerField()


    def __str__(self):
        return f"{self.grooming_service_id.species}-{self.grooming_service_id.service_title} - {self.pet_size} - {self.fur_amount}"
    

