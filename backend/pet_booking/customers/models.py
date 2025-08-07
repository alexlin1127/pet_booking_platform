from django.db import models
from django.conf import settings

# Create your models here.

class Gender(models.TextChoices):
    MALE = 'male', '男'
    FEMALE = 'female', '女'

class Species(models.TextChoices):
    CAT = 'cat', '貓'
    DOG = 'dog', '狗'

class CustomersProfile(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('users.User', to_field='user_id', on_delete=models.CASCADE, db_index=True, related_name='customersProfiles')
    full_name = models.CharField(max_length=255, null=False, blank=False)
    gender = models.CharField(max_length=6, choices=Gender.choices, null=True, blank=True)
    # birthday = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=False, blank=False)
    address = models.CharField(max_length=512, null=True, blank=True)

    class Meta:
        db_table = 'customers_profile'

    def __str__(self):
        return f"{self.full_name} ({self.email})"


class LikeStore(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('users.User', to_field='user_id', on_delete=models.CASCADE, db_index=True, related_name='likeStores')
    store_id = models.ForeignKey('stores.Store', on_delete=models.CASCADE)

    class Meta:
        db_table = 'like_store'
        # 為 user_id + store_id 組合建立唯一約束，避免重複喜愛同一家店（如需要）
        unique_together = ('user_id', 'store_id')

    def __str__(self):
        return f"User {self.user_id} likes Store {self.stores.store_name}"

class TernaryAnswer(models.TextChoices):
    YES = 'yes', '是'
    NO = 'no', '否'
    UNCERTAIN = 'uncertain', '不確定'

class Pet(models.Model):
    user_id = models.ForeignKey('users.User', to_field='user_id', on_delete=models.CASCADE, db_index=True, related_name='pets')
    species = models.CharField(max_length=4, choices=Species.choices, null=False, blank=False)
    name = models.CharField(max_length=255, null=False, blank=False)
    gender = models.CharField(max_length=6, choices=Gender.choices, null=False, blank=False)
    breed = models.CharField(max_length=255, null=True, blank=True)
    # birthday = models.DateField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    spayed_or_neutered = models.CharField(max_length=10,
        choices=TernaryAnswer.choices,
        default=TernaryAnswer.UNCERTAIN,
        null=True,
        blank=True)
    microchip = models.CharField(max_length=10,
        choices=TernaryAnswer.choices,
        default=TernaryAnswer.UNCERTAIN,
        null=True,
        blank=True)
    last_deworming_date = models.DateField(null=True, blank=True)
    last_vaccine_date = models.DateField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    image_url = models.ImageField(upload_to='pet_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'pets'

    def __str__(self):
        return f"{self.name} ({self.species}) owned by User {self.user_id}"
